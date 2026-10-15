import os
import requests

from datetime import datetime
from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

API_URL = "https://serpapi.com/search.json"


# Only these three platforms are allowed.

ALLOWED_PLATFORMS = {
    "Booking.com": ["booking.com"],
    "Agoda": ["agoda.com", "agoda"],
    "Expedia": ["expedia.com", "expedia"]
}


# ==========================================
# 2. SEARCH GOOGLE HOTELS
# ==========================================

def search_google_hotels(preferences):

    if not SERPAPI_API_KEY:
        return {
            "success": False,
            "message": "SERPAPI_API_KEY is missing.",
            "hotels": []
        }

    required_fields = [
        "destination",
        "check_in",
        "check_out",
        "guests",
        "currency"
    ]

    for field in required_fields:

        if not preferences.get(field):
            return {
                "success": False,
                "message": f"Missing preference: {field}",
                "hotels": []
            }

    try:

        check_in = str(preferences["check_in"])
        check_out = str(preferences["check_out"])

        datetime.strptime(check_in, "%Y-%m-%d")
        datetime.strptime(check_out, "%Y-%m-%d")

        if check_out <= check_in:
            raise ValueError(
                "Check-out must be after check-in."
            )

        guests = int(preferences["guests"])

        if guests < 1:
            raise ValueError("Invalid number of guests.")

        params = {
            "engine": "google_hotels",
            "q": str(preferences["destination"]),
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": guests,
            "currency": str(
                preferences["currency"]
            ).upper(),
            "gl": preferences.get("gl", "fr"),
            "hl": "en",
            "api_key": SERPAPI_API_KEY
        }

        hotel_stars = preferences.get("hotel_stars")

        if hotel_stars:
            params["hotel_class"] = str(int(hotel_stars))

        response = requests.get(
            API_URL,
            params=params,
            timeout=45
        )

        response.raise_for_status()

        data = response.json()

        if data.get("error"):
            return {
                "success": False,
                "message": data["error"],
                "hotels": []
            }

        properties = data.get("properties", [])

        hotels = []

        for property_data in properties:

            total_rate = property_data.get(
                "total_rate"
            ) or {}

            nightly_rate = property_data.get(
                "rate_per_night"
            ) or {}

            total_price = total_rate.get(
                "extracted_lowest"
            )

            nightly_price = nightly_rate.get(
                "extracted_lowest"
            )

            if total_price is None:
                continue

            total_price = float(total_price)

            if total_price <= 0:
                continue

            hotel = {

                "hotel_name": property_data.get(
                    "name",
                    "Unknown Hotel"
                ),

                "stars": property_data.get(
                    "extracted_hotel_class"
                ),

                "rating": property_data.get(
                    "overall_rating"
                ),

                "reviews": property_data.get(
                    "reviews"
                ),

                "total_price": total_price,

                "nightly_price": nightly_price,

                "currency": params["currency"],

                "amenities": property_data.get(
                    "amenities", []
                ),

                "hotel_link": property_data.get(
                    "link"
                ),

                "property_token": property_data.get(
                    "property_token"
                ),

                "property_details_link": property_data.get(
                    "serpapi_property_details_link"
                ),

                "source": "Google Hotels via SerpAPI",

                "last_checked": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

            hotels.append(hotel)

        return {
            "success": True,
            "message": f"Found {len(hotels)} hotels.",
            "hotels": hotels,
            "search_parameters": data.get(
                "search_parameters", {}
            )
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "message": f"API request failed: {error}",
            "hotels": []
        }

    except (ValueError, TypeError) as error:

        return {
            "success": False,
            "message": str(error),
            "hotels": []
        }


# ==========================================
# 3. GET HOTEL PROPERTY DETAILS
# ==========================================

def get_hotel_property_details(
    property_token,
    preferences,
    property_details_link=None
):

    if not SERPAPI_API_KEY:
        return {
            "success": False,
            "message": "SerpAPI key is missing."
        }

    if not property_token and not property_details_link:
        return {
            "success": False,
            "message": "Hotel property token is missing."
        }

    params = {
        "engine": "google_hotels",
        "property_token": property_token,
        "check_in_date": str(preferences["check_in"]),
        "check_out_date": str(preferences["check_out"]),
        "adults": int(preferences["guests"]),
        "currency": str(preferences["currency"]).upper(),
        "gl": preferences.get("gl", "fr"),
        "hl": "en",
        "api_key": SERPAPI_API_KEY
    }

    try:

        # Use the property-details link when available.

        if property_details_link:

            response = requests.get(
                property_details_link,
                params={"api_key": SERPAPI_API_KEY},
                timeout=45
            )

        else:

            response = requests.get(
                API_URL,
                params=params,
                timeout=45
            )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            return {
                "success": False,
                "message": "Unexpected SerpAPI response."
            }

        if data.get("error"):
            return {
                "success": False,
                "message": data["error"]
            }

        return {
            "success": True,
            "message": "Property details retrieved successfully.",
            "details": data
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "message": f"Property request failed: {error}"
        }

    except (ValueError, TypeError, KeyError) as error:

        return {
            "success": False,
            "message": f"Unable to process property details: {error}"
        }


# ==========================================
# 4. FIND PROVIDER OFFERS IN API RESPONSE
# ==========================================

def extract_provider_offers(data):

    offers = []

    def search_recursively(item):

        if isinstance(item, list):

            for element in item:
                search_recursively(element)

        elif isinstance(item, dict):

            # A provider offer generally has a source
            # and price information.

            if item.get("source"):

                has_price = any(
                    key in item
                    for key in [
                        "total_rate",
                        "price",
                        "total_price"
                    ]
                )

                if has_price:
                    offers.append(item)

            for value in item.values():

                if isinstance(value, (dict, list)):
                    search_recursively(value)

    search_recursively(data)

    return offers


# ==========================================
# 5. FILTER BOOKING.COM, AGODA AND EXPEDIA
# ==========================================

def filter_allowed_platforms(details):

    results = {
        "Booking.com": [],
        "Agoda": [],
        "Expedia": []
    }

    if not isinstance(details, dict):
        return results

    all_offers = extract_provider_offers(details)

    seen = set()

    for offer in all_offers:

        provider = str(
            offer.get("source", "")
        ).lower().strip()

        booking_link = str(
            offer.get("link", "")
        )

        matched_platform = None

        # Match only the three permitted providers.

        for platform, keywords in ALLOWED_PLATFORMS.items():

            if any(
                keyword in provider
                for keyword in keywords
            ):
                matched_platform = platform
                break

        if not matched_platform:
            continue

        # Extract total price.

        total_rate = offer.get("total_rate")

        if isinstance(total_rate, dict):

            price = total_rate.get(
                "extracted_lowest"
            )

        else:

            price = total_rate

        if price is None:
            price = offer.get("total_price")

        if price is None:
            price = offer.get("price")

        try:
            price = float(price)
        except (ValueError, TypeError):
            continue

        if price <= 0:
            continue

        # Avoid duplicate offers.

        offer_key = (
            matched_platform,
            booking_link,
            price
        )

        if offer_key in seen:
            continue

        seen.add(offer_key)

        # Extract hotel name.

        hotel_name = details.get(
            "name",
            "Selected Hotel"
        )

        results[matched_platform].append({

            "hotel_name": hotel_name,

            "platform": matched_platform,

            "total_price": price,

            "currency": str(
                offer.get(
                    "currency",
                    details.get("currency", "EUR")
                )
            ).upper(),

            "guests": offer.get("num_guests"),

            "free_cancellation": offer.get(
                "free_cancellation"
            ),

            "booking_link": booking_link,

            "source": provider

        })

    # Sort offers from cheapest to most expensive.

    for platform in results:

        results[platform].sort(
            key=lambda item: item["total_price"]
        )

    return results