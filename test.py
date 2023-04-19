import os
import json
import glob
import datetime
import numpy as np
import pandas as pd
import re


def get_json_files():
    while True:
        # folder_path = input("Enter dda folder path: ")
        folder_path = "dda_json"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if not folder_path.endswith(os.path.sep):
                folder_path += os.path.sep

            json_files = glob.glob(os.path.join(folder_path, '*.json'))

            if len(json_files) == 0:
                print("No JSON files found\n")
                return None
            else:
                json_files_arr = []
                print(f'Found {len(json_files)} JSON files:')

                for json_file in json_files:
                    print(json_file)

                    with open(json_file, 'r') as file:
                        data = json.load(file)
                        if "dda" in data:
                            main_json_marketdata = data
                        else:
                            json_files_arr.append(data)
                print("\n")
                return main_json_marketdata, json_files_arr
        else:
            print("Invalid path\n")
            return None


main_json, individual_jsons_arr = get_json_files()


def helper_change_value_to_compare(value, format = None):
    if value == 'INTEGER':
        value = int
    elif value == 'STRING':
        value = str
    elif value == 'DOUBLE':
        value = np.float64

    return value


def date_type_check(value, format = None):
    format = convert_format(format)
    try:
        datetime.datetime.strptime(value, format)
        print("Valid date format")
    except ValueError:
        print("Invalid date format")

# date_type_check('2012-02-11')


# DD-MMM-YY

# pomijamy rozróżnienie w między datami np. 01 i 1
def convert_format(custom_format):
    custom_format = custom_format.replace("YYYY", "%Y")
    custom_format = custom_format.replace("yyyy", "%Y")
    custom_format = custom_format.replace("MMM", "%b")
    custom_format = custom_format.replace("mmm", "%b")
    custom_format = custom_format.replace("MM", "%m")
    custom_format = custom_format.replace("mm", "%m")
    custom_format = custom_format.replace("YY", "%y")
    custom_format = custom_format.replace("yy", "%y")
    custom_format = custom_format.replace("DD", "%d")
    custom_format = custom_format.replace("dd", "%d")
    return custom_format


print(date_type_check('13-Jan-19', 'DD-MMM-YY'))


def helper_check_csv(json_file = 'dda_json/contoption.json', csv_file = None):
    print(json_file)
    for atribute in json_file:
        print(atribute['name'])
    return None


# helper_check_csv()


def check_csv(json_list, csv_list):
    for i in range(len(json_list)):
        helper_check_csv(json_list[i], csv_list[i])


def load_csv_from_folder(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        if not folder_path.endswith(os.path.sep):
            folder_path += os.path.sep
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

        if len(csv_files) == 0:
            print("No CSV files found")
            return None
        else:
            dataframes = []
            print(f'Found {len(csv_files)} JSON files:')
            for file in csv_files:
                print(file)
                dataframe = pd.read_csv(file)
                dataframes.append(dataframe)
            return dataframes
    else:
        print("Invalid path")
        return None



folder_path = "datasets"
dataframes = load_csv_from_folder(folder_path)
print(dataframes)

# Display the number of loaded dataframes
print(f"Loaded {len(dataframes)} dataframes.")
