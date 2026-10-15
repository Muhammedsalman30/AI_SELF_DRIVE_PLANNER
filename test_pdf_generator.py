from modules.itinerary_generator import (
    generate_itinerary,
    display_itinerary
)

from modules.pdf_generator import generate_itinerary_pdf


# 1. Customer information
customer_preferences = {
    "customer_name": "Salman",
    "travellers": 2,
    "travel_days": 5,
    "budget": 20000
}


# 2. Starting location
starting_location = {
    "destination_id": "PAR",
    "destination_name": "Paris"
}


# 3. Circular route
route = ["PAR", "LYO", "STR", "PAR"]


# 4. Driving information
route_details = [
    {
        "origin": "Paris",
        "destination": "Lyon",
        "distance_km": 466.05,
        "duration_minutes": 282.6
    },
    {
        "origin": "Lyon",
        "destination": "Strasbourg",
        "distance_km": 491.2,
        "duration_minutes": 288
    },
    {
        "origin": "Strasbourg",
        "destination": "Paris",
        "distance_km": 488.14,
        "duration_minutes": 310
    }
]


# 5. Selected attractions
attractions = {
    "PAR": [
        {"attraction_name": "Eiffel Tower"},
        {"attraction_name": "Notre-Dame Cathedral"}
    ],
    "LYO": [
        {"attraction_name": "Basilica of Notre-Dame de Fourvière"}
    ],
    "STR": [
        {"attraction_name": "Petite France"}
    ]
}


# 6. Hotel preferences
hotel_preferences = {
    "destination": "Paris",
    "check_in": "2026-11-12",
    "check_out": "2026-11-14",
    "guests": 2,
    "rooms": 1,
    "hotel_stars": 3,
    "currency": "EUR"
}


# 7. Matching hotels (fictional test data)
hotels = [
    {
        "hotel_name": "City Stay Paris",
        "platform": "Agoda",
        "hotel_stars": 3,
        "final_total": 380,
        "price_per_night": 190,
        "currency": "EUR",
        "last_checked": "2026-10-14"
    },
    {
        "hotel_name": "Paris Comfort Hotel",
        "platform": "Booking.com",
        "hotel_stars": 3,
        "final_total": 420,
        "price_per_night": 210,
        "currency": "EUR",
        "last_checked": "2026-10-14"
    },
    {
        "hotel_name": "Paris Central Hotel",
        "platform": "Agoda",
        "hotel_stars": 3,
        "final_total": 440,
        "price_per_night": 220,
        "currency": "EUR",
        "last_checked": "2026-10-14"
    }
]


# 8. Generate itinerary
itinerary = generate_itinerary(
    customer_preferences,
    starting_location,
    route,
    route_details,
    attractions,
    hotel_preferences,
    hotels
)


# 9. Display itinerary
display_itinerary(itinerary)


# 10. Generate PDF
pdf_path = generate_itinerary_pdf(itinerary)

print("\nPDF CREATED SUCCESSFULLY!")
print("PDF location:", pdf_path)