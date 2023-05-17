from datetime import datetime
from tools import date_format_standardization, change_type_to_compare
import logging
import os
from tools import logger_function
import json
import csv
import numpy as np
import datetime

logger_function()
log = logging.getLogger(__name__)


# function to check if datasets names and extensions match with main_dda information
def check_datasets_names_and_extensions(directory, json_file) -> None:
    for file_info in json_file["datasets"]:
        filename = file_info['name']
        extension = 'csv'
        if not os.path.isfile(os.path.join(directory, f'{filename}.{extension}')):
            log.warning(f'There is missing file {filename}.{extension}')
        else:
            for file in os.listdir(directory):
                real_extension = os.path.splitext(file)[1][1:]
            # real_extension = os.path.splitext(os.path.join(directory, filename + '.csv'))[1][1:]
                if real_extension != extension:
                    log.warning(f'Incorrect extension in {filename}.{extension}')


# function to change the date format (before checking the file)
def date_format_check(date, format) -> None:
    format_standardized = date_format_standardization(format)
    try:
        datetime.strptime(date, format_standardized)
        print("Valid date format")
    except ValueError:
        # log.warning(f'Invalid date format')
        print("Invalid date format")


# sprawdz nazwy kolumn
def check_column_names(dataframe, json_file):
    # csv -> pandas
    df_columns = list(dataframe.columns)
    del df_columns[0]
    for column in range(len(json_file)):
        if json_file[column]["name"] != df_columns[column]:
            # blad powinien byc rozwiniety jescze o nazwe pliku i nazwe kolumny
            log.warning(f"Wrong column name in ... column name :  {json_file[column]['name']}")


'''
# DO naprawy
def check_column_types(dataframe, json_file):
    # csv -> pandas
    df_types = list(dataframe.dtypes)
    print(dataframe.dtypes)
    del df_types[0]
    for type in range(len(json_file)):
        if change_type_to_compare(json_file[type]["type"]) != df_types[type]:
            print(f"typ z json: {json_file[type]['type']}, z json po konwersji: {change_type_to_compare(json_file[type]['type'])}, df.type:{df_types[type]}")
            # Dodac nazwe datasetu
            log.warning(f"Wrong column type in ... column name :  {json_file[type]['name']}")
'''


# sprawdz wartosci w kolumnach
def check_dataframe_types(dataframe, json_file):
    df_columns = list(dataframe.columns)
    del df_columns[0]
    
    for ind, column_name in enumerate(df_columns):
        expected_type = json_file[ind]["type"]
        try:
            expected_date_pattern = json_file[ind]["time_format"]
        except KeyError:
            pass

        if expected_type is None:
            raise ValueError(f"No type information found for column '{column_name}' in the JSON file.")
        
        # Check the type of each value in the column
        # Add log information
        values = dataframe[column_name]
        if expected_type == 'STRING' and not values.apply(lambda x: isinstance(x, str)).all():
            log.warning(f"Wrong value type in {column_name}. Correct type is {expected_type}")
        elif expected_type == 'DATE' and not values.apply(lambda x: isinstance(x, datetime.date)).all():
            log.warning(f"Wrong value type in {column_name}. Correct type is {expected_type}")
        elif expected_type == 'DOUBLE' and not values.apply(lambda x: isinstance(x, float)).all():
            log.warning(f"Wrong value type in {column_name}. Correct type is {expected_type}")
        elif expected_type == 'INTEGER' and not values.apply(lambda x: isinstance(x, int)).all():
            log.warning(f"Wrong value type in {column_name}. Correct type is {expected_type}")
    
    return True  # All values in all columns are of the correct types

