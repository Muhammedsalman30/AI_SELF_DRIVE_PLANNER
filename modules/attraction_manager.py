from database.destination_manager import get_attractions_by_destination


def get_route_attractions(route):

    print("\n========== ATTRACTION SELECTION ==========")

    route_attractions = {}

    # Remove duplicate destinations and final return location
    unique_destinations = list(dict.fromkeys(route[:-1]))

    for destination_id in unique_destinations:

        attractions = get_attractions_by_destination(destination_id)

        print(f"\nDestination: {destination_id}")

        if not attractions:
            print("No attractions available.")
            continue

        for index, attraction in enumerate(attractions, start=1):

            print(
                f"{index}. {attraction['attraction_name']}"
            )

        while True:

            selection = input(
                "\nEnter attraction numbers separated by commas "
                "(example: 1,2): "
            ).strip()

            try:
                selected_numbers = [
                    int(number.strip())
                    for number in selection.split(",")
                    if number.strip()
                ]

                if (
                    not selected_numbers
                    or len(selected_numbers) != len(set(selected_numbers))
                    or any(
                        number < 1 or number > len(attractions)
                        for number in selected_numbers
                    )
                ):
                    print("Invalid selection. Please try again.")
                    continue

                selected_attractions = [
                    attractions[number - 1]
                    for number in selected_numbers
                ]

                route_attractions[destination_id] = selected_attractions

                break

            except ValueError:
                print("Please enter valid attraction numbers.")

    return route_attractions