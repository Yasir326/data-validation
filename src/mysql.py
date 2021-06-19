import sqlite3
import csv
import sys
from src.helpers.helper_methods import does_file_exist

folder_name = sys.argv[1]


def create_connection():
    try:
        connection = sqlite3.connect("members_data.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS  members(aims, name, jamaat)")
        return connection
    except sqlite3.Error as e:
        exit(f"❌ ERROR: {e}")


def insert_data(master_aims_file):
    insert_failures = False
    try:
        with create_connection() as connection:
            with open(master_aims_file, newline="") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                cursor = connection.cursor()
                cursor.executemany(
                    "INSERT OR IGNORE INTO members VALUES (?, ?, ?)",
                    ((r[0], r[1], r[6]) for r in reader),  # id, name, branch
                )
                connection.commit()
                print(
                    f"✅ Successfully inserted {header[0]} {header[1]} {header[6]} data to database"
                )
    except sqlite3.Error as e:
        insert_failures = True
        exit(f"❌ ERROR in insert_data(): {e}")
    return insert_failures


def output_non_matches(output_csv, gdpr_file_csv):
    output_failures = False
    with create_connection() as connection:
        f = does_file_exist(output_csv)
    output = csv.DictWriter(
        f,
        fieldnames=[
            "aims",
            "gdpr_name",
            "master_name",
            "date",
            "time",
            "jamaat",
        ],
    )
    output.writeheader()
    with open(gdpr_file_csv, newline="", encoding="latin1") as csvfile:
        reader = csv.reader(csvfile)
        cursor = connection.cursor()

        for row in reader:
            if folder_name == "rishta-nata" or folder_name == "wasiyat":
                aims, gdpr_name, date, time = row[1], row[2], row[4], row[5]
            elif (
                folder_name == "personal-data-adult" or folder_name == "waqfe-nau-adult"
            ):
                aims, gdpr_name, date, time = row[2], row[3], row[5], row[6]
            else:
                aims, gdpr_name, date, time = (
                    row[2],
                    row[3],
                    row[7],
                    row[8],
                )
            try:
                cursor.execute(
                    "SELECT name, jamaat FROM members WHERE aims = ? AND name <> ?",
                    (aims, gdpr_name),
                )
            except sqlite3.Error as e:
                output_failures = True
                exit(f"❌ ERROR in output_non_matches: {e}")

            result = cursor.fetchone()
            if result is not None:
                output.writerow(
                    {
                        "jamaat": result[1],
                        "aims": aims,
                        "gdpr_name": gdpr_name,
                        "master_name": result[0],
                        "date": date,
                        "time": time,
                    }
                )
        print(f"✅ Successfully outputted mismatches to {output_csv}")
        return output_failures
