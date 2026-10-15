from urllib.parse import urlencode, quote


def generate_hotel_search_links(preferences):

    destination = preferences["destination"]
    check_in = preferences["check_in"]
    check_out = preferences["check_out"]
    guests = preferences["guests"]
    rooms = preferences["rooms"]

    print("\n========== HOTEL SEARCH LINKS ==========")

    # Booking.com
    booking_params = {
        "ss": destination,
        "checkin": check_in,
        "checkout": check_out,
        "group_adults": guests,
        "no_rooms": rooms,
        "group_children": 0
    }

    booking_url = (
        "https://www.booking.com/searchresults.html?"
        + urlencode(booking_params)
    )

    # Agoda
    agoda_url = (
        "https://www.agoda.com/search?"
        + urlencode({
            "city": destination,
            "checkIn": check_in,
            "checkOut": check_out,
            "adults": guests,
            "rooms": rooms
        })
    )

    # Expedia
    expedia_url = (
        "https://www.expedia.com/Hotel-Search?"
        + urlencode({
            "destination": destination,
            "startDate": check_in,
            "endDate": check_out,
            "adults": guests,
            "rooms": rooms
        })
    )

    links = {
        "Booking.com": booking_url,
        "Agoda": agoda_url,
        "Expedia": expedia_url
    }

    for platform, url in links.items():
        print(f"\n{platform}:")
        print(url)

    return links