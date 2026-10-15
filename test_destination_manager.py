from modules.starting_location import select_starting_location

selected_countries = ["FR"]

starting_location = select_starting_location(selected_countries)

print("\n========== STARTING LOCATION DETAILS ==========")

if starting_location:
    print("Destination ID:", starting_location["destination_id"])
    print("Destination:", starting_location["destination_name"])
    print("Country ID:", starting_location["country_id"])