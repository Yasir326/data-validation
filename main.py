import os
import earthpy as et
import sys
from src.mysql import insert_data, output_non_matches
from src.compile_csv import combine_csv_files
from src.split_and_merge import final_merged_file
from src.helpers.helper_methods import set_home_path, configure_master_and_gdpr_files

home_path = et.io.HOME
folder_name = sys.argv[1]
match_type = sys.argv[2]


master_aims_file, gdpr_file_csv = configure_master_and_gdpr_files(folder_name)


if __name__ == "__main__":
    # print("🏁 Finding names which do not match aims in master aims file")
    # if (folder_name == "personal-data") or (folder_name == "waqfe-nau"):
    #     final_merged_file()
    # elif (folder_name == "wasiyat") or (folder_name == "rishta-nata"):
    #     combine_csv_files()
    # else:
    #     exit(
    #         "❌ Incorrect data type selected please enter one of the following: personal-data, waqfe-nau, wasiyat or rishta-nata"
    #     )

    files_path = set_home_path(folder_name)
    os.chdir(files_path)

    insert_failures = insert_data(master_aims_file)
    if insert_failures:
        print(
            "⚠️ There were errors in inserting data into database, read above for more info"
        )

    output_failures = output_non_matches(f"{folder_name}-{match_type}.csv", gdpr_file_csv)

    if output_failures:
        print(
            "⚠️ There were errors in finding non matching data, read above for more info"
        )
    os.remove(os.path.join(files_path, "members_data.db"))
    # os.remove(os.path.join(files_path, f"{folder_name}-combined-csv.csv"))
    exit(
        f"✅ mismatches found and have been outputted to {folder_name}-mismatches.csv in the {folder_name} folder"
    )
