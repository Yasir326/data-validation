import os
import earthpy as et
import sys
from src.mysql import insert_data, output_non_matches
from src.compile_csv import combine_csv_files
from src.split_and_merge import final_merged_file

home_path = et.io.HOME
file_path = home_path, "data_validation", "src", "files"
folder_name = sys.argv[1]


def configure_file_path():
    master_aims_file = os.path.join(file_path, "main_offline_validation.csv")
    gdpr_file_csv = os.path.join(
        file_path, folder_name, folder_name + "-combined-csv.csv"
    )
    return master_aims_file, gdpr_file_csv


master_aims_file, gdpr_file_csv = configure_file_path()


if __name__ == "__main__":
    print("🏁 Finding names which do not match aims in master aims file")
    if (folder_name == "personal-data") or (folder_name == "waqfe-nau"):
        final_merged_file()
    else:
        combine_csv_files()

    output_csv = os.path.join(
        home_path, "src", "files", folder_name, folder_name + "-mismatch_output.csv"
    )

    insert_failures = insert_data(master_aims_file)
    if insert_failures:
        exit(
            "⚠️ There were errors in inserting data into database, read above for more info"
        )
    output_failures = output_non_matches(output_csv, gdpr_file_csv)

    if output_failures:
        exit(
            "⚠️ There were errors in finding non matching data, read above for more info"
        )
    os.remove(os.path.join(home_path, "data_validation", "members_data.db"))
    exit(
        f"✅ mismatches found and have been outputted to {output_csv} in the {folder_name} folder"
    )
