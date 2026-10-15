from modules.google_maps import get_driving_route

print("\n========== GOOGLE MAPS ROUTE TEST ==========")

result = get_driving_route("PAR", "LYO")

if result["success"]:

    print("\nRoute successfully calculated!")

    print("Starting location:", result["origin"])
    print("Destination:", result["destination"])
    print("Driving distance:", result["distance_km"], "KM")
    print("Estimated driving time:", result["duration_minutes"], "Minutes")

else:

    print("\nRoute calculation failed!")
    print("Reason:", result["message"])