from database.destination_manager import get_all_countries

countries = get_all_countries()

print("Countries retrieved:", len(countries))
print(countries)

for country in countries:
    print(country["country_name"], country["country_id"])