import sys
import os
import pandas as pd
from helpers.set_home_path import set_home_path
from pandas.core.groupby.groupby import DataError
'''
This module takes the combined_csv.csv file which is created by the compile_csv.py module and 
splits them into two csv files based on whetherthe Jamaat member is under or over 13. 
It then combines the files again and ensures that all the headers and rows are the same.
Should ONLY be used for the combined_csv.csv in the personal-data and waqfe-nau folders
'''
folder_name = sys.argv[1]


def return_csv_file():
    if folder_name != 'personal-data' or folder_name is 'waqfe-nau':
        exit(
            "❌ folder name must be personal-data or waqfe-nau"
        )
    else:
        csv_file = set_home_path(os.path.join(folder_name, 'combined_csv.csv'))

    return csv_file


def split_csv():
    csv_file = return_csv_file()
    data = pd.read_csv(csv_file)
    age_group = data['Age Group'].unique()
    age_group = age_group.tolist()

    for i, value in enumerate(age_group):
        try:
            data[data['Age Group'] == value].to_csv(
                f'age_group_{value}.csv', index=False, na_rep='N/A')
        except DataError as e:
            exit(f"❌ Error occurred, unable to combine csv files due to: {e}")
    print(
        f"✅ Successfully split {age_group[0]} and {age_group[1]} into separate files"
    )


split_csv()
