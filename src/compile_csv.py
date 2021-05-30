import os
import glob
import sys
import earthpy as et
import pandas as pd
from pandas.core.groupby.groupby import DataError

'''
This module takes all csv files in a given folder (which is passed as an argument)
and combines them into a single csv called 'combined_csv.csv' file within the same folder
'''

home_path = et.io.HOME
folder_name = sys.argv[1]


# Find home directory
def set_home_path(home_path):
    if not os.path.exists(home_path):
        exit("❌ Home path does not exist")
    files_path = os.path.join(home_path, "data_validation",
                              "src", "files", folder_name)
    return files_path


# combine all csv files in csv folder
def get_all_csv_files():
    files_path = set_home_path(home_path)

    if not os.path.exists(files_path):
        exit("❌ File path does not exist")
    else:
        os.chdir(files_path)

    all_files = [i for i in glob.glob('*.csv')]
    return all_files


def combine_csv_files():
    all_files = get_all_csv_files()
    try:
        combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
        combined_csv.to_csv("combined_csv.csv",
                            index=False, encoding='utf-8-sig')
        print(
            f"✅ Successfully combined all csv files in {folder_name} folder to file called combined.csv"
        )
    except DataError as e:
        exit(f"❌ Error occurred, unable to combine csv files due to: {e}")
