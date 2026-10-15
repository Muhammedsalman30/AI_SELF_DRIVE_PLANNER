from modules.route_validator import validate_circular_route


# Test 1: Valid circular route
valid_route = ["PAR", "BRU", "AMS", "LUX", "STR", "PAR"]

print("\n========== TEST 1 ==========")

result = validate_circular_route(valid_route)

print(result)


# Test 2: Invalid route
invalid_route = ["PAR", "BRU", "AMS", "ROM"]

print("\n========== TEST 2 ==========")

result = validate_circular_route(invalid_route)

print(result)


# Test 3: Invalid destination
unknown_route = ["PAR", "ABC", "PAR"]

print("\n========== TEST 3 ==========")

result = validate_circular_route(unknown_route)

print(result)


# Test 4: Empty route
empty_route = []

print("\n========== TEST 4 ==========")

result = validate_circular_route(empty_route)

print(result)