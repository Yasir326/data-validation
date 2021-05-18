import csv
import pandas as pd


# Convert Main File from xlsx to csv
master_file = "src/files/main_offline_validation.xlsx"
master_file_csv = "src/files/main_offline_validation.csv"
gdpr_file_csv = "src/files/AMA-UK-–-WASAYA-PERSONAL-DATA-CONSENT-FORM-FOR-AMJ-INTERNATIONAL-1620046642.csv"


def convert_xslx_to_csv():
    read_file = pd.read_excel(master_file)
    read_file.to_csv(master_file_csv,
                     index=None,
                     header=True)


def return_csv_as_lists():
    master_data = []
    gdpr_data = []
    with open(master_file_csv) as ms:
        root = csv.reader(ms)
        rows_master = {}
        for i in root:
            rows_master[i[0]] = i
            if "AIMS No" in rows_master:
                del rows_master["AIMS No"]

    for key, values in rows_master.items():
        master_data.append(values)

    with open(gdpr_file_csv) as gd:
        root = csv.reader(gd, delimiter=',', quotechar='"')
        rows_validation = {}
        for i in root:
            rows_validation[i[0]] = i
            if "AIMS (MEMBERSHIP) ID " in rows_validation:
                del rows_validation["AIMS (MEMBERSHIP) ID "]

        for key, values in rows_validation.items():
            gdpr_data.append(values)

    return master_data, gdpr_data


# check if the name associated with the Aims ID Match
def same_values():
    lst1, lst2 = return_csv_as_lists()
    list = []
    min_lengh = min(len(lst1), len(lst2))
    max_lengh = max(len(lst1), len(lst2))

    for i in range(max_lengh):
        # if lst1[i][0] == lst2[i][0]:
        #     print(f'ONE => {lst1[i]}, TWO => {lst2[i]}')

        # Generate new file (csv or xlsx) with data that does not match
        # Should Have the fields, Aims Name and Jamaat
        # convert_xslx_to_csv()
