import sqlite3

database_path = "data/travel_backup.db"

try:
    connection = sqlite3.connect(database_path)

    connection.execute("PRAGMA integrity_check")

    result = connection.execute(
        "PRAGMA integrity_check"
    ).fetchone()

    print("Backup integrity:", result[0])

    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    print("Tables:", tables)

    connection.close()

except sqlite3.DatabaseError as error:
    print("Backup error:", error)