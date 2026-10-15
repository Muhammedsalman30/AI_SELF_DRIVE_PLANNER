from modules.serpapi_hotel_search import search_google_hotels

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

if result["success"]:

    print("\nGOOGLE HOTELS SEARCH SUCCESSFUL!")
    print(f"Found {len(result['hotels'])} hotels.")

    for index, hotel in enumerate(result["hotels"], start=1):

        print("\n" + "-" * 40)
        print(f"Hotel {index}")

        print("Name:", hotel.get("hotel_name", "Unknown"))
        print("Stars:", hotel.get("stars", "Unknown"))
        print("Rating:", hotel.get("rating", "Unknown"))
        print("Total price:", hotel.get("total_price", "Not available"))
        print("Currency:", hotel.get("currency", "EUR"))
        print("Booking link:", hotel.get("hotel_link", "Not available"))

        # Display provider offers safely
        print(
            "Provider offers:",
            hotel.get("hotel_offers", [])
        )

else:

    print("Hotel search failed:")
    print(result["message"])