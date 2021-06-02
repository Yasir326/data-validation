import os
import earthpy as et


home_path = et.io.HOME


def set_home_path(folder_name):
    if not os.path.exists(home_path):
        exit("❌ Home path does not exist")
    files_path = os.path.join(home_path, "data_validation", "src", "files", folder_name)
    return files_path


def does_file_exist(filename):
    if os.path.isfile(filename):
        f = open(filename, "w")
    else:
        f = open(filename, "x")
    return f
