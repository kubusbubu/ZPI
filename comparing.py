from datetime import datetime
from tools import date_format_standardization
import logging
import os
from tools import logger_function

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


# outpuy_dir = [pliki_csv]
def check_column_names(dataframe, json_file):
    # csv -> pandas
    df_columns = list(dataframe.columns)
    del df_columns[0]
    for column in range(len(json_file)):
        if json_file[column]["name"] != df_columns[column]:
            # blad powinien byc rozwiniety jescze o nazwe pliku i nazwe kolumny
            log.warning("Wrong column name in " + " dataframe, column name : " + json_file[column]["name"])


def check_column_types(dataframe, json_file):
    # csv -> pandas
    df_columns = list(dataframe.columns)
    del df_columns[0]
    for column in range(len(json_file)):
        if json_file[column]["type"] != df_columns[column]:
            # blad powinien byc rozwiniety jescze o nazwe pliku i nazwe kolumny
            log.warning("Wrong column name in " + " dataframe, column name : " + json_file[column]["name"])