from database.destination_manager import get_all_countries


def get_customer_preferences():

    print("\n========== SELF-DRIVE TOUR PLANNER ==========")

    # Customer details
    customer_name = input("\nEnter customer name: ").strip()

    # Travel duration
    while True:

        try:
            days = int(input("Number of travel days: "))

            if days > 0:
                break

            print("Travel days must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")

    # Travellers
    while True:

        try:
            travellers = int(input("Number of travellers: "))

            if travellers > 0:
                break

            print("Travellers must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")

    # Budget
    while True:

        try:
            budget = float(input("Total travel budget (€): "))

            if budget > 0:
                break

            print("Budget must be greater than zero.")

        except ValueError:
            print("Please enter a valid budget.")

    # Get countries only from database
    countries = get_all_countries()

    print("\nAvailable countries:")

    for country in countries:
        print(
            country["country_id"],
            "-",
            country["country_name"]
        )

    # Country selection
    while True:

        selected_countries = input(
            "\nEnter country IDs separated by commas (example: FR,BE,NL): "
        ).upper()

        selected_countries = [
            country.strip()
            for country in selected_countries.split(",")
            if country.strip()
        ]

        available_ids = {
            country["country_id"]
            for country in countries
        }

        if (
            selected_countries
            and all(
                country in available_ids
                for country in selected_countries
            )
            and len(selected_countries) == len(set(selected_countries))
        ):
            break

        print("Invalid selection. Choose country IDs from the displayed list.")

    # Hotel preferences
    print("\n========== HOTEL PREFERENCES ==========")

    hotel_stars = 3

    breakfast = input("Breakfast required? (yes/no): ").lower().strip()

    parking = input("Parking required? (yes/no): ").lower().strip()

    if breakfast not in ["yes", "no"]:
        print("Invalid breakfast choice. Using yes.")
        breakfast = "yes"

    if parking not in ["yes", "no"]:
        print("Invalid parking choice. Using yes.")
        parking = "yes"

    preferences = {

        "customer_name": customer_name,

        "travel_days": days,

        "travellers": travellers,

        "budget": budget,

        "selected_countries": selected_countries,

        "hotel_stars": hotel_stars,

        "breakfast_required": breakfast == "yes",

        "parking_required": parking == "yes"

    }

    return preferences


if __name__ == "__main__":

    customer = get_customer_preferences()

    print("\n========== CUSTOMER PREFERENCES ==========")

    for key, value in customer.items():

        print(f"{key}: {value}")