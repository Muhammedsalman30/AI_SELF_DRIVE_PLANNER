import os
import requests
import streamlit as st

from dotenv import load_dotenv
from database.destination_manager import get_destination_coordinates


# Load local .env file
load_dotenv()

# Google Maps Routes API URL
GOOGLE_MAPS_URL = (
    "https://routes.googleapis.com/directions/v2:computeRoutes"
)


# Read API key from Streamlit Cloud Secrets or local .env
try:
    API_KEY = (
        st.secrets.get("GOOGLE_MAPS_API_KEY")
        or os.getenv("GOOGLE_MAPS_API_KEY")
    )
except Exception:
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_driving_route(origin_id, destination_id):

    # Check API key
    if not API_KEY:
        return {
            "success": False,
            "message": (
                "Google Maps API key not found. "
                "Check your .env file or Streamlit Cloud Secrets."
            )
        }

    # Get origin and destination coordinates from database
    origin = get_destination_coordinates(origin_id)
    destination = get_destination_coordinates(destination_id)

    if not origin or not destination:
        return {
            "success": False,
            "message": "Origin or destination not found in database."
        }

    # Google Maps request payload
    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin["latitude"],
                    "longitude": origin["longitude"]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination["latitude"],
                    "longitude": destination["longitude"]
                }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }

    try:

        # Send request to Google Maps Routes API
        response = requests.post(
            GOOGLE_MAPS_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        # Check API response
        if response.status_code != 200:
            return {
                "success": False,
                "message": (
                    f"Google Maps API error: "
                    f"{response.status_code} - {response.text}"
                )
            }

        data = response.json()

        routes = data.get("routes", [])

        if not routes:
            return {
                "success": False,
                "message": "No driving route found."
            }

        # Get first available route
        route = routes[0]

        # Calculate distance
        distance_km = route["distanceMeters"] / 1000

        # Calculate duration
        duration_seconds = int(
            route["duration"].replace("s", "")
        )

        duration_minutes = duration_seconds / 60

        # Return route details
        return {
            "success": True,
            "origin": origin["destination_name"],
            "destination": destination["destination_name"],
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_minutes, 2)
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": "Google Maps request timed out."
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "message": f"Connection error: {error}"
        }

    except (KeyError, ValueError, TypeError) as error:

        return {
            "success": False,
            "message": f"Unexpected API response: {error}"
        }