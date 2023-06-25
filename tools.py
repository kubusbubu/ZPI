import numpy as np
import tarfile
import os
import json
import glob
import logging
import pandas as pd
from datetime import datetime


# create tar file for testing
def create_tar_file(directory, output_filename):
    with tarfile.open(output_filename, "w") as tar:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                tar.add(file_path, arcname=os.path.basename(file_path))
    print('Tar file sucessfully created')


# change value type before checking files (consistency)
def convert_string_to_format(value):
    if value == 'INTEGER':
        value = int
    elif value == 'STRING':
        value = str
    elif value == 'DOUBLE':
        value = np.float64
    return value


def date_format_check(value, format):
    format = convert_format(format)
    try:
        datetime.strptime(value, format)
        return True
    except ValueError:
        return False


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


# function to unpack the contents of the tar file
def tar_unpack():
    # unpacks tar file
    tar_file_path = input("Enter path to tar file: ")
    output_dir_path = 'tar_output_dir'
    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extractall(output_dir_path)
    return output_dir_path


# funckja do zapisania plikow csv z danej sciezki do listy z ramkami pandas
def load_multiple_csv_to_dataframes(directory):
    dataframes = []
    filenames = os.listdir(directory)
    for filename in filenames:
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                dataframes.append(df)
    return dataframes, filenames


# function to download dda files and store them in memory
def get_json_files():
    while True:
        # folder_path = input("Enter dda folder path: ")
        folder_path = 'dda_json'
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if not folder_path.endswith(os.path.sep):
                folder_path += os.path.sep

            json_files = glob.glob(os.path.join(folder_path, '*.json'))

            if len(json_files) == 0:
                print("No JSON files found")
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

                return main_json_marketdata, json_files_arr
        else:
            print("Invalid path")
            return None


def logger_function():
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a")


def clear_logger() -> None:
    log_file = 'log.log'
    try:
        if os.path.exists(log_file):
            with open(log_file, 'w'):
                pass
        else:
            print(f"Log file '{log_file}' does not exist.")
    except IOError as e:
        print(f"An error occurred while clearing the log file: {e}")


def change_type_to_compare(value):
    if value == 'INTEGER':
        value = np.int64
    elif value == 'STRING':
        value = object
    elif value == 'DOUBLE':
        value = np.float64
    return value