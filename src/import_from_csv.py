import csv
import sqlite3
import sys

master_file = "src/files/main_offline_validation.xlsx"
master_file_csv = "src/files/main_offline_validation.csv"
gdpr_file_csv = "src/files/AMA-UK-–-WASAYA-PERSONAL-DATA-CONSENT-FORM-FOR-AMJ-INTERNATIONAL-1620046642.csv"


connection = sqlite3.connect("members_data.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS  members(id, name, branch)"
)


def insert_data():
    with open(master_file_csv, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        cursor = connection.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO members VALUES (?, ?, ?)",
            ((r[0], r[1], r[5]) for r in reader),  # id, name, branch
        )


insert_data()


def output_non_matches():
    output = csv.DictWriter(
        sys.stdout, fieldnames=["id", "gdpr_name", "master_name", "location"]
    )
    output.writeheader()
    with open(gdpr_file_csv, newline="") as csvfile:
        reader = csv.reader(csvfile)
        cursor = connection.cursor()
        for row in reader:
            id, gdpr_name = row[0], row[2]
            cursor.execute(
                "SELECT name, branch FROM members WHERE id = ? AND name <> ?",
                (id, gdpr_name),
            )
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


output_non_matches()
