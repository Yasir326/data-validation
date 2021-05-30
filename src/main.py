import csv
import sqlite3
import os
import sys

master_file = "src/files/main_offline_validation.xlsx"
master_file_csv = "src/files/main_offline_validation.csv"
gdpr_file_csv = "src/files/" + sys.argv[1] + ".csv"
output_csv = "src/files/output.csv"


def create_connection():
    try:
        connection = sqlite3.connect("members_data.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS  members(aims, name, jamaat)"
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
        exit(f"❌ ERROR in insert_data(): {e}")


insert_data()


def output_non_matches():
    with create_connection() as connection:
        f = open(output_csv, 'w')
    output = csv.DictWriter(
        f, fieldnames=["aims", "gdpr_name", "master_name", "jamaat"]
    )
    output.writeheader()
    with open(gdpr_file_csv, newline="") as csvfile:
        reader = csv.reader(csvfile)
        cursor = connection.cursor()

        for row in reader:
            if "AMA-UK-–-WASAYA" in gdpr_file_csv:
                aims, gdpr_name = row[0], row[2]
            else:
                aims, gdpr_name = row[1], row[3]
            try:
                cursor.execute(
                    "SELECT name, jamaat FROM members WHERE aims = ? AND name <> ?",
                    (aims, gdpr_name),
                )
            except sqlite3.Error as e:
                exit(f"❌ ERROR in output_non_matches: {e}")

            result = cursor.fetchone()
            if result is not None:
                output.writerow(
                    {
                        "aims": aims,
                        "gdpr_name": gdpr_name,
                        "master_name": result[0],
                        "jamaat": result[1],
                    }
                )
        print(
            f"✅ Successfully outputted mismatches to out.csv"
        )


output_non_matches()
os.remove("/Users/yasirk/data_validation/members_data.db")
