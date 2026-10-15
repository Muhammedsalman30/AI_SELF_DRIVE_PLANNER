from modules.customer_preferences import get_customer_preferences


customer = get_customer_preferences()

print("\n========== FINAL CUSTOMER DETAILS ==========")

for key, value in customer.items():

    print(f"{key}: {value}")