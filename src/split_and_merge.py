import sys
import os
import csv
import pandas as pd
from src.compile_csv import combine_csv_files
from src.helpers.helper_methods import set_home_path, does_file_exist
from pandas.core.groupby.groupby import DataError

"""
This module takes the combined-csv.csv file which is created by the compile_csv.py module and
splits them into two csv files based on whetherthe Jamaat member is under or over 13.
It then combines the files again and ensures that all the headers and rows are the same.
Should ONLY be used for the combined-csv.csvsv.csv in the personal-data and waqfe-nau folders
"""
folder_name = sys.argv[1]
files_to_delete = []


def return_csv_file(filename):
    if (folder_name != "personal-data") and (folder_name != "waqfe-nau"):
        exit("❌ folder name must be personal-data or waqfe-nau")
    else:
        files_path = set_home_path(folder_name)
        csv_file = os.path.join(files_path, filename)
        os.chdir(files_path)

    return csv_file


def split_csv():
    csv_file = return_csv_file(f"{folder_name}-combined-csv.csv")
    data = pd.read_csv(csv_file)
    age_group = data["Age Group"].unique()
    age_group = age_group.tolist()

    for i, value in enumerate(age_group):
        try:
            data[data["Age Group"] == value].to_csv(
                f"age_group_{value}.csv", index=False, na_rep="N/A"
            )
        except DataError as e:
            exit(f"❌ Error occurred, unable to combine csv files due to: {e}")
    print(
        f"✅ Successfully split {age_group[0]} and {age_group[1]} into separate files")
    os.remove(csv_file)


# Adjust under 13 csv to match data in over 13 csv
def adjust_under13s_csv():
    f = does_file_exist(return_csv_file(f"{folder_name}-combined-csv.csv"))
    output = csv.DictWriter(f, fieldnames=["aims", "name"])
    output.writeheader()
    unders_13s = return_csv_file("age_group_Under 13.csv")
    files_to_delete.append("age_group_Under 13.csv")

    with open(unders_13s, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aims, name = (
                row["Child-AIMS (MEMBERSHIP) ID"],
                row["Child-YOUR FULL NAME (First)"],
            )
            try:
                output.writerow(
                    {
                        "aims": int(float(aims)),
                        "name": name,
                    }
                )
            except csv.Error as e:
                exit(
                    f"❌ Error occurred, unable to write to output.csv files due to: {e}"
                )
    print("✅ Successfully added under 13s aims and name to output.csv")


def append_over13s_to_output():
    f = does_file_exist(return_csv_file(f"{folder_name}-combined-csv.csv"))
    output = csv.DictWriter(f, fieldnames=["aims", "name"])
    over_13s = return_csv_file("age_group_13 and over.csv")
    files_to_delete.append("age_group_13 and over.csv")

    with open(over_13s, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aims, name = (
                row["Adult-AIMS (MEMBERSHIP) ID"],
                row["Adult-YOUR FULL NAME (First)"],
            )
            try:
                output.writerow(
                    {
                        "aims": int(float(aims)),
                        "name": name,
                    }
                )
            except csv.Error as e:
                exit(
                    f"❌ Error occurred, unable to write to {folder_name}-combined-csv.csv files due to: {e}"
                )

    print("✅ Successfully appended over13s aims and name to output.csv")


def final_merged_file():
    combine_csv_files()
    split_csv()
    adjust_under13s_csv()
    append_over13s_to_output()

    for i in range(len(files_to_delete)):
        os.remove(files_to_delete[i])
