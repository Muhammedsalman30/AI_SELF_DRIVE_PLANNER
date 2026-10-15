import sqlite3
import os

# Get project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
DB_PATH = os.path.join(BASE_DIR, "data", "travel.db")


# Connect to database
def get_connection():

    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row

        return connection

    except sqlite3.Error as error:

        print("Database connection error:", error)

        return None


# Test database connection
def test_connection():

    connection = get_connection()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = cursor.fetchall()

        print("\nDATABASE CONNECTED SUCCESSFULLY!")

        print("\nAvailable tables:")

        if not tables:
            print("No tables found!")

        for table in tables:

            table_name = table["name"]

            print(f"\nTable: {table_name}")

            cursor.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            )

            count = cursor.fetchone()[0]

            print("Total records:", count)

    except sqlite3.Error as error:

        print("Database error:", error)

    finally:

        connection.close()


# Run program
if __name__ == "__main__":

    test_connection()