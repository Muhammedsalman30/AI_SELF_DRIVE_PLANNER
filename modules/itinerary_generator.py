def generate_itinerary(
    customer_preferences,
    starting_location,
    route,
    route_details,
    attractions,
    hotel_preferences,
    hotels
):
    """
    Generate a complete European self-drive travel itinerary.
    """

    # --------------------------------
    # 1. Validate circular route
    # --------------------------------

    if not route or len(route) < 3 or route[0] != route[-1]:
        raise ValueError("Invalid circular route.")

    # --------------------------------
    # 2. Calculate driving information
    # --------------------------------

    total_distance = sum(
        leg.get("distance_km", 0)
        for leg in route_details
    )

    total_driving_minutes = sum(
        leg.get("duration_minutes", 0)
        for leg in route_details
    )

    driving_hours = round(total_driving_minutes / 60, 2)

    # --------------------------------
    # 3. Prepare attractions
    # --------------------------------

    selected_attractions = {}

    for destination_id, attraction_list in attractions.items():

        selected_attractions[destination_id] = [
            attraction.get("attraction_name", "Unknown attraction")
            for attraction in attraction_list
        ]

    # --------------------------------
    # 4. Prepare hotel information
    # --------------------------------

    hotel_options = []

    for hotel in hotels:

        hotel_options.append({
            "hotel_name": hotel.get("hotel_name", "Unknown Hotel"),

            "platform": hotel.get("platform", "Unknown"),

            "hotel_stars": hotel.get(
                "hotel_stars",
                hotel.get("stars", 0)
            ),

            "total_price": hotel.get(
                "final_total",
                hotel.get("total_price", 0)
            ),

            "price_per_night": hotel.get("price_per_night", 0),

            "currency": hotel.get("currency", "EUR"),

            "last_checked": hotel.get(
                "last_checked",
                "Retrieved from Google Hotels"
            )
        })

    # --------------------------------
    # 5. Create complete itinerary
    # --------------------------------

    itinerary = {

        "customer": {
            "name": customer_preferences.get("customer_name", ""),
            "travellers": customer_preferences.get("travellers", 2),
            "budget": customer_preferences.get("budget", 0)
        },

        "starting_location": starting_location.get(
            "destination_name", "Unknown"
        ),

        "travel_days": customer_preferences.get("travel_days", 0),

        "circular_route": route,

        "route_details": route_details,

        "driving_summary": {
            "total_distance_km": round(total_distance, 2),
            "total_driving_hours": driving_hours
        },

        "selected_attractions": selected_attractions,

        "hotel_preferences": hotel_preferences,

        "hotel_options": hotel_options,

        "hotel_data_status": (
            "Hotel offers retrieved from Google Hotels "
            "and filtered to Booking.com, Agoda and Expedia. "
            "Availability and final booking prices should be "
            "confirmed with the provider."
        )
    }

    return itinerary


# --------------------------------
# DISPLAY ITINERARY
# --------------------------------

def display_itinerary(itinerary):

    print("\n========== TRAVEL ITINERARY ==========")

    print("\nCustomer:", itinerary["customer"]["name"])

    print("Starting Location:", itinerary["starting_location"])

    print("Travel Days:", itinerary["travel_days"])

    print("\nCircular Route:")

    print(" -> ".join(itinerary["circular_route"]))

    print("\nDriving Summary:")

    print(
        "Total Distance:",
        itinerary["driving_summary"]["total_distance_km"],
        "KM"
    )

    print(
        "Total Driving Hours:",
        itinerary["driving_summary"]["total_driving_hours"]
    )

    print("\nHotel Options:")

    for hotel in itinerary["hotel_options"]:

        print("\nHotel:", hotel["hotel_name"])
        print("Platform:", hotel["platform"])
        print("Stars:", hotel["hotel_stars"])
        print("Total Price:", hotel["total_price"], hotel["currency"])

    print("\n======================================")