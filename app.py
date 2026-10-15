import streamlit as st

from database.destination_manager import get_all_countries
from modules.route_calculator import calculate_complete_route
from modules.route_validator import validate_circular_route
from datetime import date, timedelta
from modules.hotel_search import generate_hotel_search_links
from modules.hotel_comparator import compare_hotels
from modules.itinerary_generator import generate_itinerary
from modules.pdf_generator import generate_itinerary_pdf
from modules.serpapi_hotel_search import (
    search_google_hotels,
    get_hotel_property_details,
    filter_allowed_platforms
)

def clear_session_data(keys):
    """
    Remove outdated session data when the user changes selections.
    """
    for key in keys:
        st.session_state.pop(key, None)


# Clear everything after customer preferences change
def clear_after_customer_change():
    clear_session_data([
        "starting_location",
        "selected_route",
        "selected_attractions",
        "driving_result",
        "hotel_preferences",
        "hotel_search_links",
        "best_hotels",
        "generated_itinerary",
        "generated_pdf_path"
    ])


# Clear route-related data after starting location changes
def clear_after_start_change():
    clear_session_data([
        "selected_route",
        "selected_attractions",
        "driving_result",
        "hotel_preferences",
        "hotel_search_links",
        "best_hotels",
        "generated_itinerary",
        "generated_pdf_path"
    ])


# Clear downstream data after route changes
def clear_after_route_change():
    clear_session_data([
        "selected_attractions",
        "driving_result",
        "hotel_preferences",
        "hotel_search_links",
        "best_hotels",
        "generated_itinerary",
        "generated_pdf_path"
    ])


# Clear hotel results after hotel preferences change
def clear_after_hotel_change():
    clear_session_data([
        "hotel_search_links",
        "best_hotels",
        "generated_itinerary",
        "generated_pdf_path"
    ])

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Europe Self-Drive Planner",
    page_icon="🚗",
    layout="wide"
)


# --------------------------------
# APPLICATION HEADER
# --------------------------------

st.title("🚗 Europe Self-Drive Travel Planner")

st.write(
    "Plan your European road trip, select destinations, "
    "explore attractions and compare hotel options."
)

st.divider()


# --------------------------------
# CUSTOMER DETAILS
# --------------------------------

st.header("1. Customer Travel Details")

with st.form("customer_details_form"):

    customer_name = st.text_input("Customer Name")

    col1, col2 = st.columns(2)

    with col1:
        travel_days = st.number_input(
            "Number of Travel Days",
            min_value=1,
            max_value=30,
            value=5
        )

        travellers = st.number_input(
            "Number of Travellers",
            min_value=1,
            max_value=20,
            value=2
        )

    with col2:
        budget = st.number_input(
            "Total Travel Budget (€)",
            min_value=1.0,
            value=2000.0,
            step=100.0
        )

    st.subheader("Select Countries")

    countries = get_all_countries()

    country_options = {
        country["country_name"]: country["country_id"]
        for country in countries
    }

    selected_country_names = st.multiselect(
        "Choose the countries you want to visit",
        options=list(country_options.keys())
    )

    selected_country_ids = [
        country_options[name]
        for name in selected_country_names
    ]

    submitted = st.form_submit_button(
        "Save Travel Preferences"
    )


# --------------------------------
# SAVE CUSTOMER DETAILS
# --------------------------------

if submitted:

    if not customer_name.strip():
        st.error("Please enter your name.")

    elif not selected_country_ids:
        st.error("Please select at least one country.")

    else:

        st.session_state["customer_preferences"] = {
            "customer_name": customer_name.strip(),
            "travel_days": int(travel_days),
            "travellers": int(travellers),
            "budget": float(budget),
            "selected_countries": selected_country_ids,
            "hotel_stars": 3,
            "breakfast_required": False,
            "parking_required": False
        }

        st.success("Travel preferences saved successfully!")

        st.write("### Your Saved Details")

        st.json(
            st.session_state["customer_preferences"]
        )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "Europe Self-Drive Travel Planner | "
    "Python • Streamlit • SQLite • Google Maps"
)

# --------------------------------
# STARTING DESTINATION SELECTION
# --------------------------------

from database.destination_manager import get_all_destinations

if "customer_preferences" in st.session_state:

    st.divider()

    st.header("2. Select Starting Destination")

    preferences = st.session_state["customer_preferences"]

    all_destinations = get_all_destinations()

    available_destinations = [
        destination
        for destination in all_destinations
        if destination["country_id"] in preferences["selected_countries"]
    ]

    destination_options = {
        destination["destination_name"]: destination["destination_id"]
        for destination in available_destinations
    }

    selected_start_name = st.selectbox(
        "Choose your starting city",
        options=list(destination_options.keys())
    )

    if st.button("Confirm Starting Destination"):

        selected_start_id = destination_options[selected_start_name]

        st.session_state["starting_location"] = {
            "destination_id": selected_start_id,
            "destination_name": selected_start_name
        }

        st.success(
            f"Starting destination selected: {selected_start_name}"
        )

        st.json(st.session_state["starting_location"])

# --------------------------------
# CIRCULAR ROUTE SELECTION
# --------------------------------

from modules.route_validator import validate_circular_route

if "starting_location" in st.session_state:

    st.divider()

    st.header("3. Build Your Circular Route")

    start = st.session_state["starting_location"]

    st.write(
        f"Your trip starts and ends in **{start['destination_name']}**."
    )

    # Exclude the starting city from intermediate choices
    other_destinations = [
        destination
        for destination in available_destinations
        if destination["destination_id"] != start["destination_id"]
    ]

    destination_options = {
        destination["destination_name"]: destination["destination_id"]
        for destination in other_destinations
    }

    selected_city_names = st.multiselect(
        "Select the cities you want to visit",
        options=list(destination_options.keys()),
        max_selections=max(0, min(10, preferences["travel_days"] - 1))
    )

    if st.button("Generate Circular Route"):

        selected_city_ids = [
            destination_options[name]
            for name in selected_city_names
        ]

        route = [
            start["destination_id"]
        ] + selected_city_ids + [
            start["destination_id"]
        ]

        validation = validate_circular_route(route)

        if validation["valid"]:

            st.session_state["selected_route"] = route

            st.success("Circular route generated successfully!")

            route_names = [
                start["destination_name"]
            ]

            for city_id in selected_city_ids:
                city = next(
                    (
                        destination
                        for destination in other_destinations
                        if destination["destination_id"] == city_id
                    ),
                    None
                )

                if city:
                    route_names.append(city["destination_name"])

            route_names.append(start["destination_name"])

            st.subheader("Your Travel Route")

            st.write(" → ".join(route_names))

            st.json(route)

        else:
            st.error(validation["message"])


# --------------------------------
# TOURIST ATTRACTION SELECTION
# --------------------------------

from database.destination_manager import get_attractions_by_destination

if "selected_route" in st.session_state:

    st.divider()

    st.header("4. Select Tourist Attractions")

    route = st.session_state["selected_route"]

    selected_attractions = {}

    # Exclude the final repeated starting location
    for destination_id in route[:-1]:

        attractions = get_attractions_by_destination(destination_id)

        if not attractions:
            st.warning(
                f"No attractions available for {destination_id}."
            )
            continue

        destination_name = next(
            (
                destination["destination_name"]
                for destination in available_destinations
                if destination["destination_id"] == destination_id
            ),
            destination_id
        )

        st.subheader(destination_name)

        attraction_options = {
            attraction["attraction_name"]: attraction
            for attraction in attractions
        }

        selected_names = st.multiselect(
            f"Choose attractions in {destination_name}",
            options=list(attraction_options.keys()),
            key=f"attractions_{destination_id}"
        )

        selected_attractions[destination_id] = [
            attraction_options[name]
            for name in selected_names
        ]

    if st.button("Save Selected Attractions"):

        st.session_state["selected_attractions"] = (
            selected_attractions
        )

        st.success("Tourist attractions saved successfully!")

        st.write("### Your Selected Attractions")

        for destination_id, attraction_list in (
            selected_attractions.items()
        ):

            st.write(f"**{destination_id}**")

            if attraction_list:
                for attraction in attraction_list:
                    st.write(
                        "- " + attraction["attraction_name"]
                    )
            else:
                st.write("No attractions selected.")

# --------------------------------
# GOOGLE MAPS DRIVING INFORMATION
# --------------------------------

if "selected_route" in st.session_state:

    st.divider()

    st.header("5. Google Maps Driving Information")

    route = st.session_state["selected_route"]

    if st.button("Calculate Driving Distance"):

        # Validate circular route before calling Google Maps
        validation = validate_circular_route(route)

        if not validation["valid"]:

            st.error(validation["message"])

        else:

            with st.spinner("Calculating driving distance..."):

                try:

                    result = calculate_complete_route(route)

                    if result:

                        st.session_state["driving_result"] = result

                        st.success(
                            "Driving information calculated successfully!"
                        )

                    else:

                        st.error(
                            "Unable to calculate driving information."
                        )

                except Exception as error:

                    st.error(f"Google Maps error: {error}")


    # Display calculated information
    if "driving_result" in st.session_state:

        result = st.session_state["driving_result"]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Driving Distance",
                f'{result["total_distance_km"]} KM'
            )

        with col2:

            st.metric(
                "Total Driving Time",
                f'{result["total_duration_minutes"] / 60:.2f} Hours'
            )

        st.subheader("Route Details")

        for leg in result["route_details"]:

            st.write(
                f'**{leg["origin"]} → {leg["destination"]}**'
            )

            st.write(
                f'Distance: {leg["distance_km"]} KM'
            )

            st.write(
                f'Driving time: {leg["duration_minutes"]:.1f} minutes'
            )

            st.divider()

# --------------------------------
# HOTEL PREFERENCES
# --------------------------------

if "selected_route" in st.session_state:

    st.divider()

    st.header("6. Hotel Search Preferences")

    route = st.session_state["selected_route"]

    # Exclude the repeated starting destination
    route_destinations = route[:-1]

    destination_names = {
        destination["destination_id"]: destination["destination_name"]
        for destination in available_destinations
    }

    hotel_destinations = [
        destination_names[destination_id]
        for destination_id in route_destinations
        if destination_id in destination_names
    ]

    with st.form("hotel_preferences_form"):

        hotel_destination = st.selectbox(
            "Select Hotel Destination",
            options=hotel_destinations
        )

        col1, col2 = st.columns(2)

        with col1:

            check_in = st.date_input(
                "Check-in Date",
                value=date.today() + timedelta(days=30),
                min_value=date.today()
            )

            guests = st.number_input(
                "Number of Guests",
                min_value=1,
                max_value=20,
                value=2
            )

            hotel_stars = st.selectbox(
                "Hotel Category",
                options=[1, 2, 3, 4, 5],
                index=2,
                format_func=lambda x: f"{x} Stars"
            )

        with col2:

            check_out = st.date_input(
                "Check-out Date",
                value=date.today() + timedelta(days=32),
                min_value=date.today() + timedelta(days=1)
            )

            rooms = st.number_input(
                "Number of Rooms",
                min_value=1,
                max_value=10,
                value=1
            )

        st.subheader("Required Hotel Facilities")

        col3, col4 = st.columns(2)

        with col3:

            breakfast = st.checkbox("Breakfast Required")

            wifi = st.checkbox(
                "Wi-Fi Required",
                value=True
            )

            private_bathroom = st.checkbox(
                "Private Bathroom Required",
                value=True
            )

        with col4:

            parking = st.checkbox("Parking Required")

            free_cancellation = st.checkbox(
                "Free Cancellation Required",
                value=True
            )

        maximum_budget = st.number_input(
            "Maximum Total Hotel Budget (€)",
            min_value=1.0,
            value=500.0,
            step=50.0
        )

        hotel_submitted = st.form_submit_button(
            "Save Hotel Preferences"
        )

    if hotel_submitted:

        if check_out <= check_in:

            st.error(
                "Check-out date must be after check-in date."
            )

        else:

            hotel_preferences = {

                "destination": hotel_destination,

                "check_in": check_in.strftime("%Y-%m-%d"),

                "check_out": check_out.strftime("%Y-%m-%d"),

                "guests": int(guests),

                "rooms": int(rooms),

                "hotel_stars": hotel_stars,

                "breakfast_required": breakfast,

                "parking_required": parking,

                "wifi_required": wifi,

                "private_bathroom_required": private_bathroom,

                "free_cancellation_required": free_cancellation,

                "maximum_budget": float(maximum_budget),

                "currency": "EUR"
            }

            st.session_state["hotel_preferences"] = (
                hotel_preferences
            )

            st.success(
                "Hotel preferences saved successfully!"
            )

            st.write("### Your Hotel Requirements")

            st.json(hotel_preferences)

# --------------------------------
# HOTEL SEARCH AND COMPARISON
# --------------------------------

if "hotel_preferences" in st.session_state:

    st.divider()

    st.header("7. Hotel Search and Comparison")

    preferences = st.session_state["hotel_preferences"]

    st.subheader("Search Hotel Platforms")

    if st.button("Generate Hotel Search Links"):

        links = generate_hotel_search_links(preferences)

        st.session_state["hotel_search_links"] = links

    if "hotel_search_links" in st.session_state:

        links = st.session_state["hotel_search_links"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.link_button(
                "Booking.com",
                links["Booking.com"],
                use_container_width=True
            )

        with col2:
            st.link_button(
                "Agoda",
                links["Agoda"],
                use_container_width=True
            )

        with col3:
            st.link_button(
                "Expedia",
                links["Expedia"],
                use_container_width=True
            )

    st.divider()

    # st.subheader("Enter Hotel Offers")

    # st.info(
    #     "Enter hotel details collected from the booking platforms. "
    #     "Use the final price for the complete stay, including taxes and fees."
    # )

    # with st.form("hotel_comparison_form"):

    #     number_of_hotels = st.number_input(
    #         "Number of hotel offers",
    #         min_value=1,
    #         max_value=20,
    #         value=3
    #     )

    #     hotel_records = []

    #     for index in range(int(number_of_hotels)):

    #         st.markdown(f"### Hotel Offer {index + 1}")

    #         hotel_name = st.text_input(
    #             "Hotel Name",
    #             key=f"hotel_name_{index}"
    #         )

    #         platform = st.selectbox(
    #             "Booking Platform",
    #             ["Booking.com", "Agoda", "Expedia"],
    #             key=f"platform_{index}"
    #         )

    #         stars = st.selectbox(
    #             "Hotel Stars",
    #             [1, 2, 3, 4, 5],
    #             index=2,
    #             key=f"stars_{index}"
    #         )

    #         base_price = st.number_input(
    #             "Base Price (€)",
    #             min_value=0.0,
    #             value=300.0,
    #             key=f"base_price_{index}"
    #         )

    #         taxes = st.number_input(
    #             "Taxes and Fees (€)",
    #             min_value=0.0,
    #             value=0.0,
    #             key=f"taxes_{index}"
    #         )

    #         breakfast = st.checkbox(
    #             "Breakfast Available",
    #             key=f"breakfast_{index}"
    #         )

    #         parking = st.checkbox(
    #             "Parking Available",
    #             key=f"parking_{index}"
    #         )

    #         wifi = st.checkbox(
    #             "Wi-Fi Available",
    #             value=True,
    #             key=f"wifi_{index}"
    #         )

    #         private_bathroom = st.checkbox(
    #             "Private Bathroom Available",
    #             value=True,
    #             key=f"bathroom_{index}"
    #         )

    #         free_cancellation = st.checkbox(
    #             "Free Cancellation Available",
    #             key=f"cancellation_{index}"
    #         )

    #         last_checked = st.date_input(
    #             "Offer Checked Date",
    #             value=date.today(),
    #             key=f"checked_{index}"
    #         )

    #         hotel_records.append({

    #             "hotel_name": hotel_name,
    #             "platform": platform,
    #             "hotel_stars": stars,

    #             "base_price": base_price,
    #             "taxes_and_fees": taxes,
    #             "currency": "EUR",

    #             "breakfast": breakfast,
    #             "parking": parking,
    #             "wifi": wifi,
    #             "private_bathroom": private_bathroom,
    #             "free_cancellation": free_cancellation,

    #             "last_checked": last_checked.isoformat()
    #         })

    #     compare_submitted = st.form_submit_button(
    #         "Compare Hotel Offers"
    #     )

    # if compare_submitted:

    #     if any(not hotel["hotel_name"].strip() for hotel in hotel_records):

    #         st.error("Please enter a hotel name for every offer.")

    #     else:

    #         best_hotels = compare_hotels(
    #             preferences,
    #             hotel_records
    # #         )

    #         st.session_state["best_hotels"] = best_hotels

    #         st.success("Hotel comparison completed!")

    # if "best_hotels" in st.session_state:

    #     best_hotels = st.session_state["best_hotels"]

    #     st.subheader("Top 3 Matching Hotels")

    #     if not best_hotels:

    #         st.warning(
    #             "No hotels match your requirements. "
    #             "Try adjusting your preferences."
    #         )

    #     else:

    #         for index, hotel in enumerate(best_hotels, start=1):

    #             with st.container(border=True):

    #                 st.markdown(
    #                     f"### {index}. {hotel['hotel_name']}"
    #                 )

    #                 col1, col2, col3 = st.columns(3)

    #                 col1.metric(
    #                     "Total Price",
    #                     f"€{hotel['final_total']:.2f}"
    #                 )

    #                 col2.metric(
    #                     "Price Per Night",
    #                     f"€{hotel['price_per_night']:.2f}"
    #                 )

    #                 col3.metric(
    #                     "Hotel Rating",
    #                     f"{hotel['hotel_stars']} Stars"
    #                 )

    #                 st.write("Platform:", hotel["platform"])

    #                 st.write(
    #                     "Breakfast:",
    #                     "Yes" if hotel["breakfast"] else "No"
    #                 )

    #                 st.write(
    #                     "Parking:",
    #                     "Yes" if hotel["parking"] else "No"
    #                 )

    #                 st.write(
    #                     "Wi-Fi:",
    #                     "Yes" if hotel["wifi"] else "No"
    #                 )

    #                 st.write(
    #                     "Private Bathroom:",
    #                     "Yes" if hotel["private_bathroom"] else "No"
    #                 )

    #                 st.write(
    #                     "Free Cancellation:",
    #                     "Yes" if hotel["free_cancellation"] else "No"
    #                 )

    #                 st.caption(
    #                     f"Offer checked: {hotel['last_checked']}"
    #                 )

    #         st.info(
    #             "These are manually entered offers. "
    #             "Confirm current availability and final prices "
    #             "with the booking platform before booking."
    #         )

# ==========================================
# ==========================================
# STEP 14: AUTOMATIC HOTEL SEARCH
# ==========================================

st.divider()

st.header("7. Automatic Hotel Search")

# Initialize session state safely

if "hotel_search_results" not in st.session_state:
    st.session_state["hotel_search_results"] = []

if "selected_hotel_details" not in st.session_state:
    st.session_state["selected_hotel_details"] = {}

if "selected_hotel_for_itinerary" not in st.session_state:
    st.session_state["selected_hotel_for_itinerary"] = None


if "hotel_preferences" in st.session_state:

    preferences = st.session_state["hotel_preferences"]

    # --------------------------------------
    # SEARCH GOOGLE HOTELS
    # --------------------------------------

    if st.button("Search Available Hotels"):

        with st.spinner("Searching Google Hotels through SerpAPI..."):

            result = search_google_hotels(preferences)

            if result.get("success"):

                st.session_state["hotel_search_results"] = (
                    result.get("hotels", [])
                )

                st.session_state["selected_hotel_details"] = {}

                st.session_state["selected_hotel_for_itinerary"] = None

                st.session_state.pop("generated_itinerary", None)
                st.session_state.pop("generated_pdf_path", None)

                st.success(
                    f"Found {len(result.get('hotels', []))} hotels!"
                )

            else:

                st.error(result.get("message", "Hotel search failed."))


    # --------------------------------------
    # DISPLAY GOOGLE HOTELS
    # --------------------------------------

    hotels = st.session_state["hotel_search_results"]

    if hotels:

        st.subheader("Available Google Hotels")

        hotel_names = [
            hotel["hotel_name"]
            for hotel in hotels
        ]

        selected_hotel_name = st.selectbox(
            "Select a hotel",
            options=hotel_names,
            key="selected_google_hotel"
        )

        selected_hotel = next(
            (
                hotel for hotel in hotels
                if hotel["hotel_name"] == selected_hotel_name
            ),
            None
        )

        if selected_hotel:

            st.session_state["selected_hotel_for_itinerary"] = (
                selected_hotel
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Hotel Stars",
                    selected_hotel.get("stars") or "Unknown"
                )

            with col2:
                st.metric(
                    "Guest Rating",
                    selected_hotel.get("rating") or "Unknown"
                )

            with col3:
                st.metric(
                    "Total Price",
                    f'{selected_hotel.get("total_price", 0)} '
                    f'{selected_hotel.get("currency", "EUR")}'
                )

            st.write(
                "**Hotel:**",
                selected_hotel["hotel_name"]
            )

            if selected_hotel.get("booking_link"):

                st.link_button(
                    "Visit Hotel Website",
                    selected_hotel["booking_link"]
                )

            st.caption(
                "Price shown by Google Hotels through SerpAPI. "
                "Confirm the final booking price and availability "
                "with the provider."
            )

            # --------------------------------------
            # PROPERTY DETAILS AND PLATFORM COMPARISON
            # --------------------------------------

            if st.button("Compare Booking Platforms"):

                with st.spinner("Retrieving hotel property details..."):

                    details_result = get_hotel_property_details(
                        property_token=selected_hotel.get(
                            "property_token"
                        ),
                        preferences=preferences,
                        property_details_link=selected_hotel.get(
                            "property_details_link"
                        )
                    )

                    if details_result.get("success"):

                        platform_results = filter_allowed_platforms(
                            details_result.get("details", {})
                        )

                        if not isinstance(platform_results, dict):
                            platform_results = {}

                        st.session_state["selected_hotel_details"] = (
                            platform_results
                        )

                        total_offers = sum(
                            len(offers)
                            for offers in platform_results.values()
                            if isinstance(offers, list)
                        )

                        if total_offers > 0:

                            st.success(
                                f"Found {total_offers} provider offers."
                            )

                        else:

                            st.warning(
                                "Google Hotels did not return specific "
                                "Booking.com, Agoda or Expedia offers "
                                "for this property. The Google Hotels "
                                "price is still available for your itinerary."
                            )

                    else:

                        st.error(
                            details_result.get(
                                "message",
                                "Unable to retrieve property details."
                            )
                        )


            # --------------------------------------
            # DISPLAY PLATFORM COMPARISON
            # --------------------------------------

            platform_results = st.session_state.get(
                "selected_hotel_details",
                {}
            )

            if isinstance(platform_results, dict) and platform_results:

                st.subheader("Booking Platform Comparison")

                for platform in [
                    "Booking.com",
                    "Agoda",
                    "Expedia"
                ]:

                    offers = platform_results.get(platform, [])

                    with st.expander(platform, expanded=True):

                        if offers:

                            for offer in offers:

                                st.write(
                                    "**Total Price:**",
                                    offer.get("total_price"),
                                    offer.get("currency", "EUR")
                                )

                                st.write(
                                    "**Guests:**",
                                    offer.get("guests", "Not specified")
                                )

                                if offer.get("booking_link"):

                                    st.link_button(
                                        f"Book through {platform}",
                                        offer["booking_link"]
                                    )

                        else:

                            st.info(
                                f"No {platform} offers were returned."
                            )


else:

    st.info(
        "Please complete your hotel preferences before searching."
    )


# ==========================================
# STEP 15: COMPLETE ITINERARY AND PDF
# ==========================================

st.divider()

st.header("8. Generate Your Complete Travel Itinerary")


required_keys = [
    "customer_preferences",
    "starting_location",
    "selected_route",
    "selected_attractions",
    "hotel_preferences",
    "driving_result",
    "selected_hotel_for_itinerary"
]


# Check whether all required sections are completed

if all(
    key in st.session_state
    for key in required_keys
):

    selected_hotel = st.session_state.get(
        "selected_hotel_for_itinerary"
    )

    if not isinstance(selected_hotel, dict):

        st.info(
            "Please search and select a hotel before generating "
            "your itinerary."
        )

    else:

        # --------------------------------------
        # PREPARE HOTEL INFORMATION
        # --------------------------------------

        check_in = date.fromisoformat(
            st.session_state["hotel_preferences"]["check_in"]
        )

        check_out = date.fromisoformat(
            st.session_state["hotel_preferences"]["check_out"]
        )

        nights = (check_out - check_in).days

        if nights <= 0:

            st.error(
                "Invalid hotel dates. Check-out must be after check-in."
            )

        else:

            total_price = float(
                selected_hotel.get("total_price", 0) or 0
            )

            if total_price <= 0:

                st.error(
                    "The selected hotel does not have a valid price."
                )

            else:

                # Convert the Google Hotels result into the
                # format expected by itinerary_generator.py.

                hotel_options = [

                    {
                        "hotel_name": selected_hotel.get(
                            "hotel_name",
                            "Selected Hotel"
                        ),

                        "platform": "Google Hotels (SerpAPI)",

                        "hotel_stars": selected_hotel.get(
                            "stars"
                        ) or 0,

                        "final_total": total_price,

                        "price_per_night": round(
                            total_price / nights,
                            2
                        ),

                        "currency": selected_hotel.get(
                            "currency",
                            "EUR"
                        ),

                        "last_checked": selected_hotel.get(
                            "last_checked",
                            "Not available"
                        )
                    }

                ]


                # --------------------------------------
                # GENERATE ITINERARY
                # --------------------------------------

                if st.button(
                    "Generate Travel Itinerary",
                    use_container_width=True
                ):

                    try:

                        itinerary = generate_itinerary(

                            customer_preferences=st.session_state[
                                "customer_preferences"
                            ],

                            starting_location=st.session_state[
                                "starting_location"
                            ],

                            route=st.session_state[
                                "selected_route"
                            ],

                            route_details=st.session_state[
                                "driving_result"
                            ]["route_details"],

                            attractions=st.session_state[
                                "selected_attractions"
                            ],

                            hotel_preferences=st.session_state[
                                "hotel_preferences"
                            ],

                            hotels=hotel_options

                        )


                        # Generate PDF

                        pdf_path = generate_itinerary_pdf(
                            itinerary
                        )


                        # Save results

                        st.session_state["generated_itinerary"] = (
                            itinerary
                        )

                        st.session_state["generated_pdf_path"] = (
                            pdf_path
                        )

                        st.success(
                            "Your complete travel itinerary "
                            "has been generated successfully!"
                        )


                    except Exception as error:

                        st.error(
                            f"Unable to generate itinerary: {error}"
                        )


                # --------------------------------------
                # DISPLAY ITINERARY
                # --------------------------------------

                if "generated_itinerary" in st.session_state:

                    st.subheader(
                        "Your Complete Travel Itinerary"
                    )

                    st.json(
                        st.session_state["generated_itinerary"]
                    )


                # --------------------------------------
                # DOWNLOAD PDF
                # --------------------------------------

                if "generated_pdf_path" in st.session_state:

                    pdf_path = st.session_state[
                        "generated_pdf_path"
                    ]

                    try:

                        with open(pdf_path, "rb") as pdf_file:

                            st.download_button(

                                label="📄 Download Travel Itinerary PDF",

                                data=pdf_file.read(),

                                file_name="Europe_Self_Drive_Itinerary.pdf",

                                mime="application/pdf",

                                use_container_width=True

                            )

                    except FileNotFoundError:

                        st.error(
                            "PDF file not found. Please generate "
                            "the itinerary again."
                        )

else:

    st.info(
        "Complete customer details, starting location, route, "
        "attractions, driving information, hotel preferences "
        "and hotel selection first."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Europe Self-Drive Travel Planner | "
    "Python • Streamlit • SQLite • Google Maps • SerpAPI"
)