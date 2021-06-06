import os
import sys
import earthpy as et
from src.mysql import insert_data, output_non_matches
from src.compile_csv import combine_csv_files
from src.split_and_merge import final_merged_file
from src.helpers.helper_methods import set_home_path, does_file_exist

home_path = et.io.HOME
file_path = home_path, "data_validation", "src", "files"
folder_name = sys.argv[1]


def configure_file_path():
    master_aims_file = os.path.join(
        file_path, "main_offline_validation.csv")
    output_csv = os.path.join(
        file_path, "output.csv.csv")
    gdpr_file_csv = set_home_path(folder_name + "_output.csv")
    output_csv = does_file_exist(os.path.join(
        file_path, folder_name + "_mismatch_output.csv"))
    return output_csv, master_aims_file, gdpr_file_csv


output_csv, master_aims_file, gdpr_file_csv = configure_file_path()


# def create_connection():
#     try:
#         connection = sqlite3.connect("members_data.db")
#         cursor = connection.cursor()
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS  members(aims, name, jamaat)")
#         return connection
#     except sqlite3.Error as e:
#         exit(f"❌ ERROR: {e}")


# def insert_data():
#     try:
#         with create_connection() as connection:
#             f = open(output_csv, "+r")
#             with open(master_aims_file, newline="") as csvfile:
#                 reader = csv.reader(csvfile)
#                 header = next(reader)
#                 cursor = connection.cursor()
#                 cursor.executemany(
#                     "INSERT OR IGNORE INTO members VALUES (?, ?, ?)",
#                     ((r[0], r[1], r[5]) for r in reader),  # id, name, branch
#                 )
#                 connection.commit()
#                 print(
#                     f"✅ Successfully inserted {header[0]} {header[1]} {header[5]} data to database"
#                 )
#     except sqlite3.Error as e:
#         exit(f"❌ ERROR in insert_data(): {e}")


# def output_non_matches():
#     with create_connection() as connection:
#         f = open(output_csv, "w")
#     output = csv.DictWriter(
#         f, fieldnames=["aims", "gdpr_name", "master_name", "jamaat"]
#     )
#     output.writeheader()
#     with open(gdpr_file_csv, newline="") as csvfile:
#         reader = csv.reader(csvfile)
#         cursor = connection.cursor()

#         for row in reader:
#             if "AMA-UK-–-WASAYA" in gdpr_file_csv:
#                 aims, gdpr_name = row[0], row[2]
#             else:
#                 aims, gdpr_name = row[1], row[3]
#             try:
#                 cursor.execute(
#                     "SELECT name, jamaat FROM members WHERE aims = ? AND name <> ?",
#                     (aims, gdpr_name),
#                 )
#             except sqlite3.Error as e:
#                 exit(f"❌ ERROR in output_non_matches: {e}")

#             result = cursor.fetchone()
#             if result is not None:
#                 output.writerow(
#                     {
#                         "aims": aims,
#                         "gdpr_name": gdpr_name,
#                         "master_name": result[0],
#                         "jamaat": result[1],
#                     }
#                 )
#         print(f"✅ Successfully outputted mismatches to out.csv")


if __name__ == "__main__":
    print("🏁 Finding names which do not match aims in master aims file")
    if (folder_name == "personal-data") and (folder_name == "waqfe-nau"):
        final_merged_file()
    else:
        combine_csv_files()

    insert_failures = insert_data(output_csv, master_aims_file)
    output_failures = output_non_matches(output_csv, gdpr_file_csv)

    if insert_failures or output_failures:
        exit(
            "⚠️ There were errors in finding non matching data, read above for more info"
        )
    os.remove(os.path.join(home_path, "data_validation", "members_data.db"))
    exit(
        f"✅ mismatches found and have been outputted to {output_csv} in the {folder_name} folder")
