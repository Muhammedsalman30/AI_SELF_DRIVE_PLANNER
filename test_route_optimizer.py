from modules.route_optimizer import generate_route
from modules.starting_location import select_starting_location


# Customer selections
selected_countries = ["FR"]
travel_days = 5

# Select starting location
starting_location = select_starting_location(selected_countries)

# Generate route
if starting_location:

    route = generate_route(
        selected_countries,
        starting_location,
        travel_days
    )

    print("\n========== FINAL ROUTE ==========")

    if route:
        print("Route:", " → ".join(route))
        print("Pickup location:", route[0])
        print("Return location:", route[-1])