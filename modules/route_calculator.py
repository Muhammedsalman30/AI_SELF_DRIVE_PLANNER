from modules.google_maps import get_driving_route


def calculate_complete_route(route):

    print("\n========== COMPLETE ROUTE CALCULATION ==========")

    total_distance = 0
    total_duration = 0

    route_details = []

    for index in range(len(route) - 1):

        origin_id = route[index]
        destination_id = route[index + 1]

        print(f"\nCalculating: {origin_id} → {destination_id}")

        result = get_driving_route(
            origin_id,
            destination_id
        )

        if not result["success"]:

            print("Route calculation failed!")
            print(result["message"])

            return None

        total_distance += result["distance_km"]
        total_duration += result["duration_minutes"]

        route_details.append(result)

        print("Distance:", result["distance_km"], "KM")
        print("Driving time:", result["duration_minutes"], "Minutes")

    print("\n========== TOTAL TRIP DISTANCE ==========")

    print("Total distance:", round(total_distance, 2), "KM")

    print(
        "Total driving time:",
        round(total_duration / 60, 2),
        "Hours"
    )

    return {
        "route_details": route_details,
        "total_distance_km": round(total_distance, 2),
        "total_duration_minutes": round(total_duration, 2)
    }