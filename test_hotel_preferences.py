from modules.hotel_preferences import get_hotel_preferences


hotel = get_hotel_preferences()


print("\n========== CUSTOMER HOTEL REQUIREMENTS ==========")

for key, value in hotel.items():

    print(f"{key}: {value}")