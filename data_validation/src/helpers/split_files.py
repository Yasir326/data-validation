import os
import pandas as pd
from src.helpers.helper_methods import (
    set_home_path,
    return_file_and_match_type,
)
from pandas.core.groupby.groupby import DataError

"""
Splits and outputs files based on Jamaat or branch name in matched or mismatched CSVs
"""

folder_name, match_type = return_file_and_match_type()


def return_csv_file(filename):
    files_path = set_home_path(folder_name)
    csv_file = os.path.join(files_path, filename)
    os.chdir(files_path)

    return csv_file


def split_csv():
    csv_file = return_csv_file(f"{folder_name}-{match_type}.csv")
    data = pd.read_csv(csv_file)
    jamaat_name = data["jamaat"].unique()
    jamaat_name = jamaat_name.tolist()

    for i, value in enumerate(jamaat_name):
        try:
            data[data["jamaat"] == value].to_csv(
                f"{value}-{folder_name}-{match_type}.csv", index=False, na_rep="N/A"
            )
        except DataError as e:
            exit(f"❌ Error occurred, unable to combine csv files due to: {e}")
    print(
        f"✅ Successfully split files based on Jamaat name in the {folder_name} folder"
    )
    os.remove(csv_file)
