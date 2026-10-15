from database.destination_manager import get_destination_coordinates


def validate_circular_route(route):

    """
    Validate that a self-drive route starts and ends
    at exactly the same destination ID.
    """

    if not route:

        return {
            "valid": False,
            "message": "Route cannot be empty."
        }

    # Check minimum number of locations
    if len(route) < 2:

        return {
            "valid": False,
            "message": "Route must contain a starting and ending location."
        }

    # Get starting and ending IDs
    start_location = route[0]
    end_location = route[-1]

    # Validate that all locations exist in database
    for destination_id in route:

        destination = get_destination_coordinates(destination_id)

        if destination is None:

            return {
                "valid": False,
                "message": f"Destination '{destination_id}' does not exist in your dataset."
            }

    # Check circular route
    if start_location != end_location:

        return {
            "valid": False,
            "message": "Invalid circular route! Pickup and return locations must be identical."
        }

    return {
        "valid": True,
        "message": "Valid circular route! Car pickup and return locations are identical.",
        "start_location": start_location,
        "end_location": end_location
    }