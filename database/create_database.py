import sqlite3
import pandas as pd
import os

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = BASE_DIR
DB_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "travel.db")


# ==========================================
# 2. CREATE DATABASE
# ==========================================

def create_database():

    connection = None

    try:

        print("Starting database creation...")

        # ----------------------------------
        # CHECK CSV FILES
        # ----------------------------------

        csv_files = {
            "countries": "countries.csv",
            "destinations": "destinations.csv",
            "attractions": "attractions.csv",
            "route_templates": "route_templates.csv"
        }

        dataframes = {}

        for table, filename in csv_files.items():

            file_path = os.path.join(DATA_DIR, filename)

            if not os.path.exists(file_path):
                raise FileNotFoundError(
                    f"CSV file not found: {filename}"
                )

            dataframes[table] = pd.read_csv(file_path)

            print(
                f"Loaded {filename}: "
                f"{len(dataframes[table])} records"
            )

        # ----------------------------------
        # REMOVE OLD DATABASE
        # ----------------------------------

        if os.path.exists(DB_PATH):

            os.remove(DB_PATH)

            print("\nOld database removed.")

        # ----------------------------------
        # CREATE FRESH DATABASE
        # ----------------------------------

        connection = sqlite3.connect(DB_PATH)

        # ----------------------------------
        # CREATE TABLES
        # ----------------------------------

        for table, dataframe in dataframes.items():

            dataframe.to_sql(
                table,
                connection,
                if_exists="fail",
                index=False
            )

            print(
                f"Created table: {table}"
            )

        connection.commit()

        # ----------------------------------
        # VERIFY DATABASE
        # ----------------------------------

        print("\nDATABASE CREATED SUCCESSFULLY!")

        print("\nDatabase records:")

        for table in dataframes:

            result = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()

            print(f"{table}: {result[0]}")

        # ----------------------------------
        # INTEGRITY CHECK
        # ----------------------------------

        integrity = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        print("\nDatabase integrity:", integrity)

        print("\nDatabase location:")
        print(DB_PATH)

    except Exception as error:

        print("\nDatabase creation failed:", error)

    finally:

        if connection:
            connection.close()


# ==========================================
# 3. RUN DATABASE CREATION
# ==========================================

if __name__ == "__main__":

    create_database()