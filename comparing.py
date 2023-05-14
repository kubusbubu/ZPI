from datetime import datetime
from tools import date_format_standardization
import logging
import os
from tools import logger_function
import json
import csv

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
        print("Invalid date format")


# sprawdz nazwy kolumn
def check_column_names(dataframe, json_file):
    # csv -> pandas
    df_columns = list(dataframe.columns)
    del df_columns[0]
    for column in range(len(json_file)):
        if json_file[column]["name"] != df_columns[column]:
            # blad powinien byc rozwiniety jescze o nazwe pliku i nazwe kolumny
            log.warning("Wrong column name in " + " dataframe, column name : " + json_file[column]["name"])


# sprawdz typy kolumn - > to nie bedzie dzialac
def check_column_types(dataframe, json_file):
    # csv -> pandas
    df_columns = list(dataframe.columns)
    del df_columns[0]
    for column in range(len(json_file)):
        if json_file[column]["type"] != df_columns[column]:
            # blad powinien byc rozwiniety jescze o nazwe pliku i nazwe kolumny
            log.warning("Wrong column type in " + " dataframe, column name : " + json_file[column]["name"])


# sprawdz wartosci w kolumnach
def check_dataframe_types(dataframe, json_file):
    # Read the JSON file

    # with open(json_file, 'r') as f:
    #     column_types = json.load(f)
    df_columns = list(dataframe.columns)
    del df_columns[0]
    
    for ind, column_name in enumerate(df_columns):
        # Get the expected type for the current column
        
        # expected_type = column_types.get(column_name)
        expected_type = json_file[ind]["type"]

        if expected_type is None:
            raise ValueError(f"No type information found for column '{column_name}' in the JSON file.")
        
        # Check the type of each value in the column
        # Add log information
        values = dataframe[column_name]
        if expected_type == 'STRING' and not values.apply(lambda x: isinstance(x, str)).all():
            return False
        elif expected_type == 'DATE' and not values.apply(lambda x: isinstance(x, str)).all():
            return False  # Adjust this condition based on your date format
        elif expected_type == 'DOUBLE' and not values.apply(lambda x: isinstance(x, float)).all():
            return False
        elif expected_type == 'INTEGER' and not values.apply(lambda x: isinstance(x, int)).all():
            return False
    
    return True  # All values in all columns are of the correct types

