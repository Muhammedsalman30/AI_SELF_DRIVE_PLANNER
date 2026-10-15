from datetime import datetime, date


def get_hotel_preferences():

    print("\n========== HOTEL SEARCH PREFERENCES ==========")

    # Destination
    destination = input(
        "\nEnter hotel destination: "
    ).strip()

    while not destination:
        print("Destination cannot be empty.")
        destination = input("Enter hotel destination: ").strip()

    # Check-in date
    while True:

        check_in = input(
            "Check-in date (YYYY-MM-DD): "
        ).strip()

        try:
            check_in_date = datetime.strptime(
                check_in, "%Y-%m-%d"
            ).date()

            if check_in_date < date.today():
                print("Check-in date cannot be in the past.")
                continue

            break

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

    # Check-out date
    while True:

        check_out = input(
            "Check-out date (YYYY-MM-DD): "
        ).strip()

        try:
            check_out_date = datetime.strptime(
                check_out, "%Y-%m-%d"
            ).date()

            if check_out_date <= check_in_date:
                print("Check-out must be after check-in.")
                continue

            break

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

    # Number of guests
    while True:

        try:
            guests = int(input("Number of guests: "))

            if guests > 0:
                break

            print("Guests must be greater than zero.")

        except ValueError:
            print("Enter a valid number.")

    # Number of rooms
    while True:

        try:
            rooms = int(input("Number of rooms: "))

            if rooms > 0:
                break

            print("Rooms must be greater than zero.")

        except ValueError:
            print("Enter a valid number.")

    # Hotel category
    while True:

        try:
            stars = int(
                input("Hotel category (1-5 stars): ")
            )

            if 1 <= stars <= 5:
                break

            print("Choose between 1 and 5 stars.")

        except ValueError:
            print("Enter a valid number.")

    # Yes / No preferences
    def ask_yes_no(question):

        while True:

            answer = input(
                question + " (yes/no): "
            ).strip().lower()

            if answer in ["yes", "no"]:
                return answer == "yes"

            print("Please enter yes or no.")

    breakfast = ask_yes_no("Breakfast required?")
    parking = ask_yes_no("Parking required?")
    wifi = ask_yes_no("Wi-Fi required?")
    private_bathroom = ask_yes_no("Private bathroom required?")
    free_cancellation = ask_yes_no("Free cancellation required?")

    # Maximum hotel budget
    while True:

        try:
            budget = float(
                input("Maximum hotel budget (€): ")
            )

            if budget > 0:
                break

            print("Budget must be greater than zero.")

        except ValueError:
            print("Enter a valid budget.")

    preferences = {

        "destination": destination,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "rooms": rooms,
        "hotel_stars": stars,

        "breakfast_required": breakfast,
        "parking_required": parking,
        "wifi_required": wifi,
        "private_bathroom_required": private_bathroom,
        "free_cancellation_required": free_cancellation,

        "maximum_budget": budget,
        "currency": "EUR"
    }

    return preferences


if __name__ == "__main__":

    hotel = get_hotel_preferences()

    print("\n========== FINAL HOTEL PREFERENCES ==========")

    for key, value in hotel.items():

        print(f"{key}: {value}")