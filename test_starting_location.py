from database.destination_manager import get_all_destinations

destinations = get_all_destinations()

print("\n========== DESTINATION DATA TEST ==========")

for destination in destinations:
    print(destination)

print("\nTotal destinations:", len(destinations))