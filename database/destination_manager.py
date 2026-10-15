from database.db_connection import get_connection


# 1. Get all countries
def get_all_countries():

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT country_id, country_name
            FROM countries
            ORDER BY country_name
        """)

        countries = cursor.fetchall()

        return [dict(country) for country in countries]

    except Exception as error:
        print("Error fetching countries:", error)
        return []

    finally:
        connection.close()


# 2. Get destinations by country
def get_destinations_by_country(country_id):

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                destination_id,
                destination_name,
                country_id,
                latitude,
                longitude
            FROM destinations
            WHERE country_id = ?
            ORDER BY destination_name
        """, (country_id,))

        destinations = cursor.fetchall()

        return [dict(destination) for destination in destinations]

    except Exception as error:
        print("Error fetching destinations:", error)
        return []

    finally:
        connection.close()


# 3. Get attractions by destination
def get_attractions_by_destination(destination_id):

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM attractions
            WHERE destination_id = ?
        """, (destination_id,))

        attractions = cursor.fetchall()

        return [dict(attraction) for attraction in attractions]

    except Exception as error:
        print("Error fetching attractions:", error)
        return []

    finally:
        connection.close()


# 4. Get destination coordinates
def get_destination_coordinates(destination_id):

    connection = get_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                destination_id,
                destination_name,
                latitude,
                longitude
            FROM destinations
            WHERE destination_id = ?
        """, (destination_id,))

        destination = cursor.fetchone()

        if destination:
            return dict(destination)

        return None

    except Exception as error:
        print("Error fetching coordinates:", error)
        return None

    finally:
        connection.close()


# 5. Get all destinations with country information
def get_all_destinations():

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                destination_id,
                destination_name,
                country_id,
                latitude,
                longitude
            FROM destinations
            ORDER BY destination_name
        """)

        destinations = cursor.fetchall()

        return [dict(destination) for destination in destinations]

    except Exception as error:
        print("Error fetching all destinations:", error)
        return []

    finally:
        connection.close()