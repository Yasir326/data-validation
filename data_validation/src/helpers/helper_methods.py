import os
import sys
import earthpy as et


def return_home_path():
    return et.io.HOME


def return_file_and_match_type():
    return sys.argv[1], sys.argv[2]


def set_home_path(folder_name):
    home_path = return_home_path()
    if not os.path.exists(home_path):
        exit("❌ Home path does not exist")
    files_path = os.path.join(
        home_path, "data_validation", "data_validation", "src", "files", folder_name
    )
    return files_path


def does_file_exist(filename):
    if os.path.isfile(filename):
        f = open(filename, "a")
    else:
        f = open(filename, "x")
    return f


def configure_master_and_gdpr_files(folder_name):
    home_path = return_home_path()
    master_aims_file = os.path.join(
        home_path, "data_validation", "data_validation", "src", "files", "aims-data.csv"
    )
    gdpr_file_csv = os.path.join(
        home_path,
        "data_validation",
        "data_validation",
        "src",
        "files",
        folder_name,
        f"{folder_name}.csv",
    )

    return master_aims_file, gdpr_file_csv
