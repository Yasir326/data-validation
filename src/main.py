import csv
import sqlite3
import os
from pathlib import Path

dir = Path("/Users/yasirk/data_validation")


master_file = "src/files/main_offline_validation.xlsx"
master_file_csv = "src/files/main_offline_validation.csv"
gdpr_file_csv = "src/files/AMA-UK-–-WASAYA-PERSONAL-DATA-CONSENT-FORM-FOR-AMJ-INTERNATIONAL-1620046642.csv"
output_csv = "src/files/output.csv"


def create_connection():
    try:
        connection = sqlite3.connect("members_data.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS  members(id, name, branch)"
        )
        return connection
    except sqlite3.Error as e:
        exit(f"❌ ERROR: {e}")


def insert_data():
    try:
        with create_connection() as connection:
            f = open(output_csv, '+r')
            with open(master_file_csv, newline="") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                cursor = connection.cursor()
                cursor.executemany(
                    "INSERT OR IGNORE INTO members VALUES (?, ?, ?)",
                    ((r[0], r[1], r[5]) for r in reader),  # id, name, branch
                )
                connection.commit()
                print(
                    f"✅ Successfully inserted {header[0]} {header[1]} {header[5]} data to database"
                )
    except sqlite3.Error as e:
        exit(f"❌ ERROR: {e}")


insert_data()


def output_non_matches():
    with create_connection() as connection:
        f = open(output_csv, 'w')
    output = csv.DictWriter(
        f, fieldnames=["id", "gdpr_name", "master_name", "location"]
    )
    output.writeheader()
    with open(gdpr_file_csv, newline="") as csvfile:
        reader = csv.reader(csvfile)
        cursor = connection.cursor()

        for row in reader:
            id, gdpr_name = row[0], row[2]
            try:
                cursor.execute(
                    "SELECT name, branch FROM members WHERE id = ? AND name <> ?",
                    (id, gdpr_name),
                )
            except sqlite3.Error as e:
                exit(f"❌ ERROR: {e}")

            result = cursor.fetchone()
            if result is not None:
                output.writerow(
                    {
                        "id": id,
                        "gdpr_name": gdpr_name,
                        "master_name": result[0],
                        "location": result[1],
                    }
                )
                print(
                    f"✅ Successfully outputted mismatches to out.csv"
                )


output_non_matches()
os.remove("/members_data.db")
