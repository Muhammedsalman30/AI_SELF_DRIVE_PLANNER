from database.destination_manager import get_all_destinations


def select_starting_location(selected_countries):

    print("\n========== SELECT STARTING LOCATION ==========")

    all_destinations = get_all_destinations()

    available_destinations = [
        destination
        for destination in all_destinations
        if destination["country_id"] in selected_countries
    ]

    if not available_destinations:
        print("No destinations available for selected countries.")
        return None

    print("\nAvailable starting locations:")

    for destination in available_destinations:
        print(
            destination["destination_id"],
            "-",
            destination["destination_name"]
        )

    while True:

        selected_id = input(
            "\nEnter your starting destination ID: "
        ).strip().upper()

        for destination in available_destinations:

            if destination["destination_id"] == selected_id:

                print(
                    "\nStarting location selected:",
                    destination["destination_name"]
                )

                return destination

        print("Invalid destination ID. Please choose from the list.")