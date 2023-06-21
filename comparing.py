from datetime import datetime
from tools import change_type_to_compare
import logging
import os
from tools import logger_function, date_format_check


logger_function()
log = logging.getLogger(__name__)


# function to check if datasets names and extensions match with main_dda information
def check_datasets_names_and_extensions(json_file, directory) -> None:
    for file_info in json_file["datasets"]:
        filename = file_info['name']
        extension = 'csv'
        if not os.path.isfile(os.path.join(directory, f'{filename}.{extension}')):
            log.warning(f'There is missing file {filename}.{extension}')
        else:
            for file in os.listdir(directory):
                real_extension = os.path.splitext(file)[1][1:]
                if real_extension != extension:
                    log.warning(f'Incorrect extension in {filename}.{extension}')


class Comparing:
    def __init__(self, json_file, dataframe, filename):
        self.json_file = json_file
        self.dataframe = dataframe
        self.filename = filename

    # # function to change the date format (before checking the file)
    # def date_format_check(self, date, pattern, ind) -> None:
    #     try:
    #         datetime.strptime(date, pattern)
    #     except ValueError:
    #         wrong_rows
    #         # log.warning(f'Invalid date format')


    # sprawdz nazwy kolumn
    def check_column_names(self):
        # csv -> pandas
        df_columns = list(self.dataframe.columns)
        del df_columns[0]
        for column in range(len(self.json_file)):
            if self.json_file[column]["name"] != df_columns[column]:
                log.warning(f"Wrong column name in {self.filename} column name :  {self.json_file[column]['name']}")

    def check_dataframe_types(self):
        df_columns = list(self.dataframe.columns)
        del df_columns[0]

        for ind, column_name in enumerate(df_columns):
            expected_type = self.json_file[ind]["type"]
            try:
                expected_date_pattern = self.json_file[ind]["time_format"]
            except KeyError:
                pass

            if expected_type is None:
                raise ValueError(f"No type information found for column '{column_name}' in the JSON file.")

            # Check the type of each value in the column
            # Add log information
            values = self.dataframe[column_name]
            if expected_type == 'STRING' and not values.apply(lambda x: isinstance(x, str)).all():
                log.warning(f"Wrong value type in {column_name} in {self.filename}. Correct type is {expected_type}")
                wrong_rows = []
                for ind, val in enumerate(list(values)):
                    if not isinstance(val, str):
                        wrong_rows.append(ind)
                if len(wrong_rows) != 0:
                    log.warning(f"There are wrong value types in following rows {wrong_rows} in {self.filename}")

            elif expected_type == 'DATE':
                wrong_rows = []
                for i, val in enumerate(list(values)):
                    expected_date_pattern = self.json_file[ind]["time_format"]
                    if not date_format_check(val, expected_date_pattern):
                        wrong_rows.append(i)
                if len(wrong_rows) != 0:   
                    log.warning(f"There are wrong value types in following rows {wrong_rows} in {self.filename}, should be DATE with {expected_date_pattern} format")

            elif expected_type == 'DOUBLE' and not values.apply(lambda x: isinstance(x, float)).all():
                log.warning(f"Wrong value type in {column_name} in {self.filename}. Correct type is {expected_type}")
                wrong_rows = []
                for ind, val in enumerate(list(values)):
                    if not isinstance(val, float):
                        wrong_rows.append(ind)
                if len(wrong_rows) != 0:
                    log.warning(f"There are wrong value types in following rows {wrong_rows} in {self.filename}")

            elif expected_type == 'INTEGER' and not values.apply(lambda x: isinstance(x, int)).all():
                log.warning(f"Wrong value type in {column_name} in {self.filename}. Correct type is {expected_type}")
                wrong_rows = []
                for ind, val in enumerate(list(values)):
                    if not isinstance(val, int):
                        wrong_rows.append(ind)
                if len(wrong_rows) != 0:
                    log.warning(f"There are wrong value types in following rows {wrong_rows} in {self.filename}")
        return True  # All values in all columns are of the correct types


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