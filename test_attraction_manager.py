from modules.attraction_manager import get_route_attractions

route = ["PAR", "LYO", "STR", "PAR"]

selected_attractions = get_route_attractions(route)

print("\n========== SELECTED ATTRACTIONS ==========")

for destination_id, attractions in selected_attractions.items():

    print(f"\n{destination_id}:")

    for attraction in attractions:
        print("-", attraction["attraction_name"])