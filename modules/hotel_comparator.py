from datetime import datetime


def compare_hotels(preferences, hotels):

    matching_hotels = []

    # Calculate number of nights
    check_in = datetime.strptime(
        preferences["check_in"], "%Y-%m-%d"
    ).date()

    check_out = datetime.strptime(
        preferences["check_out"], "%Y-%m-%d"
    ).date()

    nights = (check_out - check_in).days

    maximum_budget = float(preferences["maximum_budget"])
    required_currency = preferences.get("currency", "EUR").upper()

    for hotel in hotels:

        # Validate hotel rating
        if hotel["hotel_stars"] != preferences["hotel_stars"]:
            continue

        # Validate currency
        hotel_currency = hotel.get("currency", "EUR").upper()

        if hotel_currency != required_currency:
            continue

        # Get base price and additional fees
        # If only total_price is provided, treat it as the
        # complete price including taxes and fees.
        if "base_price" in hotel:
            base_price = float(hotel["base_price"])
            taxes_and_fees = float(hotel.get("taxes_and_fees", 0))
            final_total = base_price + taxes_and_fees
        else:
            final_total = float(hotel["total_price"])
            base_price = final_total
            taxes_and_fees = 0

        # Validate price
        if final_total <= 0 or taxes_and_fees < 0:
            continue

        if final_total > maximum_budget:
            continue

        # Check mandatory facilities
        if preferences["breakfast_required"] and not hotel["breakfast"]:
            continue

        if preferences["parking_required"] and not hotel["parking"]:
            continue

        if preferences["wifi_required"] and not hotel["wifi"]:
            continue

        if (
            preferences["private_bathroom_required"]
            and not hotel["private_bathroom"]
        ):
            continue

        if (
            preferences["free_cancellation_required"]
            and not hotel["free_cancellation"]
        ):
            continue

        # Create a standardized result
        matching_hotel = hotel.copy()

        matching_hotel["nights"] = nights
        matching_hotel["base_price"] = base_price
        matching_hotel["taxes_and_fees"] = taxes_and_fees
        matching_hotel["final_total"] = final_total
        matching_hotel["price_per_night"] = round(
            final_total / nights, 2
        )
        matching_hotel["last_checked"] = hotel.get(
            "last_checked", "Not provided"
        )

        matching_hotels.append(matching_hotel)

    # Rank hotels by final total price
    matching_hotels.sort(
        key=lambda hotel: hotel["final_total"]
    )

    return matching_hotels[:3]


def display_hotels(hotels):

    print("\n========== TOP 3 MATCHING HOTELS ==========")

    if not hotels:
        print("No hotels match your requirements.")
        return

    for index, hotel in enumerate(hotels, start=1):

        currency = hotel["currency"]

        print(f"\n========== HOTEL {index} ==========")

        print("Hotel:", hotel["hotel_name"])
        print("Platform:", hotel["platform"])
        print("Hotel stars:", hotel["hotel_stars"])

        print("Number of nights:", hotel["nights"])

        print("Base price:", currency, hotel["base_price"])
        print("Taxes and fees:", currency, hotel["taxes_and_fees"])

        print("Final total:", currency, hotel["final_total"])
        print("Price per night:", currency, hotel["price_per_night"])

        print("Breakfast:", hotel["breakfast"])
        print("Parking:", hotel["parking"])
        print("Wi-Fi:", hotel["wifi"])
        print("Private bathroom:", hotel["private_bathroom"])
        print("Free cancellation:", hotel["free_cancellation"])

        print("Offer last checked:", hotel["last_checked"])