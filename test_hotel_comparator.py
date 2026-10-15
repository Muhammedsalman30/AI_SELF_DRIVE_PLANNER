from modules.hotel_preferences import get_hotel_preferences
from modules.hotel_comparator import compare_hotels, display_hotels


preferences = get_hotel_preferences()


# Fictional records for testing only.
# They are not live hotel offers.

hotels = [

    {
        "hotel_name": "Paris Comfort Hotel",
        "platform": "Booking.com",
        "hotel_stars": 3,
        "base_price": 400,
        "taxes_and_fees": 20,
        "currency": "EUR",
        "breakfast": True,
        "parking": True,
        "wifi": True,
        "private_bathroom": True,
        "free_cancellation": True,
        "last_checked": "2026-10-14"
    },

    {
        "hotel_name": "City Stay Paris",
        "platform": "Agoda",
        "hotel_stars": 3,
        "base_price": 350,
        "taxes_and_fees": 30,
        "currency": "EUR",
        "breakfast": True,
        "parking": False,
        "wifi": True,
        "private_bathroom": True,
        "free_cancellation": True,
        "last_checked": "2026-10-14"
    },

    {
        "hotel_name": "Grand Paris Hotel",
        "platform": "Expedia",
        "hotel_stars": 3,
        "base_price": 500,
        "taxes_and_fees": 50,
        "currency": "EUR",
        "breakfast": True,
        "parking": True,
        "wifi": True,
        "private_bathroom": True,
        "free_cancellation": True
    },

    {
        "hotel_name": "Budget Paris Rooms",
        "platform": "Booking.com",
        "hotel_stars": 2,
        "base_price": 220,
        "taxes_and_fees": 20,
        "currency": "EUR",
        "breakfast": True,
        "parking": False,
        "wifi": True,
        "private_bathroom": True,
        "free_cancellation": True
    },

    {
        "hotel_name": "Paris Central Hotel",
        "platform": "Agoda",
        "hotel_stars": 3,
        "base_price": 400,
        "taxes_and_fees": 40,
        "currency": "EUR",
        "breakfast": True,
        "parking": False,
        "wifi": True,
        "private_bathroom": True,
        "free_cancellation": True
    }
]


best_hotels = compare_hotels(preferences, hotels)

display_hotels(best_hotels)