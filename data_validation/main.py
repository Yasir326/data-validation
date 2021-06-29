import os
from src.mysql import insert_data, output_non_matches
from src.helpers.split_files import split_csv
from src.helpers.helper_methods import (
    set_home_path,
    configure_master_and_gdpr_files,
    return_file_and_match_type,
)


folder_list = [
    "personal-data-adult",
    "personal-data-child",
    "rishta-nata",
    "waqfe-nau-adult",
    "waqfe-nau-child",
    "wasiyat",
]


if __name__ == "__main__":
    folder_name, match_type = return_file_and_match_type()
    print(f"🏁 Finding {match_type} between GDPR file and  Master AIMS file")
    master_aims_file, gdpr_file_csv = configure_master_and_gdpr_files(folder_name)

    if folder_name not in folder_list:
        exit(
            f"❌ Incorrect data type selected please enter one of the following: {folder_list}"
        )
    if match_type != "matches" and match_type != "mismatches":
        exit(
            "❌ Incorrect match type selected please enter one of the following: matches or mismatches"
        )

    files_path = set_home_path(folder_name)
    os.chdir(files_path)

    insert_failures = insert_data(master_aims_file)
    if insert_failures:
        print(
            "⚠️ There were errors in inserting data into database, read above for more info"
        )

    output_failures = output_non_matches(
        f"{folder_name}-{match_type}.csv", gdpr_file_csv, folder_name, match_type
    )

    if output_failures:
        print(
            "⚠️ There were errors in finding non matching data, read above for more info"
        )
    split_csv()
    os.remove(os.path.join(files_path, "members_data.db"))
    exit(
        f"✅ {match_type} found and outputted to {folder_name}-{match_type}.csv in the {folder_name} folder appended with Jamaat name"
    )
