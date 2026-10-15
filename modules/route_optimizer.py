from database.destination_manager import get_destinations_by_country
from modules.route_validator import validate_circular_route


def generate_route(selected_countries, starting_location, travel_days):

    print("\n========== ROUTE OPTIMIZER ==========")

    if not starting_location:
        return None

    start_id = starting_location["destination_id"]

    # Collect destinations from selected countries
    available_destinations = []

    for country_id in selected_countries:

        destinations = get_destinations_by_country(country_id)

        available_destinations.extend(destinations)

    # Remove the starting destination from the remaining list
    other_destinations = [
        destination
        for destination in available_destinations
        if destination["destination_id"] != start_id
    ]

    if not other_destinations:
        print("Not enough destinations to generate a route.")
        return None

    # Select destinations based on available travel days
    number_of_stops = min(travel_days - 1, len(other_destinations))

    selected_destinations = other_destinations[:number_of_stops]

    # Generate circular route
    route = [start_id]

    for destination in selected_destinations:
        route.append(destination["destination_id"])

    route.append(start_id)

    # Validate circular route
    validation = validate_circular_route(route)

    if not validation["valid"]:
        print("Route validation failed:", validation["message"])
        return None

    print("\nGenerated Route:")

    for destination_id in route:
        print(destination_id, end=" → ")

    print("\n\nRoute validation successful!")

    return route