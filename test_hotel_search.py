from modules.hotel_preferences import get_hotel_preferences
from modules.hotel_search import generate_hotel_search_links


# Collect customer hotel preferences
preferences = get_hotel_preferences()

# Generate hotel platform search links
hotel_links = generate_hotel_search_links(preferences)

print("\n========== HOTEL SEARCH COMPLETED ==========")
print("Total platforms:", len(hotel_links))