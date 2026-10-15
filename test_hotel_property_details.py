from modules.serpapi_hotel_search import (
    search_google_hotels,
    get_hotel_property_details,
    filter_allowed_platforms
)

preferences = {
    "destination": "Paris, France",
    "check_in": "2026-11-12",
    "check_out": "2026-11-14",
    "guests": 2,
    "currency": "EUR",
    "hotel_stars": 3,
    "free_cancellation_required": False
}

result = search_google_hotels(preferences)

if result["success"] and result["hotels"]:

    first_hotel = result["hotels"][0]

    print("\nSELECTED HOTEL:")
    print(first_hotel["hotel_name"])

    property_token = first_hotel["property_token"]

    details_result = get_hotel_property_details(
        property_token,
        preferences
    )

    if details_result["success"]:

        details = details_result["details"]

        platform_results = filter_allowed_platforms(details)

        print("\n" + "=" * 50)
        print("HOTEL PLATFORM COMPARISON")
        print("=" * 50)

        for platform, offers in platform_results.items():

            print(f"\n{platform}")

            if offers:

                for offer in offers:

                    print("Hotel:", offer["hotel_name"])
                    print("Total Price:", offer["total_price"],
                          offer["currency"])
                    print("Guests:", offer["guests"])
                    print("Booking Link:", offer["booking_link"])

            else:

                print("No matching offers available.")

    else:

        print(details_result["message"])

else:

    print("Hotel search failed:", result["message"])