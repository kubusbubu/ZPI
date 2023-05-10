from tools import logger_function, tar_unpack, date_format_standardization, get_json_files, create_tar_file, \
    load_multiple_csv_to_dataframes, clear_logger
from comparing import date_format_check, check_datasets_names_and_extensions, check_column_names
import logging


def main():
    # tworzenie testowego pliku tar
    # create_tar_file('datasets', 'output.tar')

    # open files
    main_json, individual_jsons_arr = get_json_files()
    # print('Output z get_json_files() : ', '\nMain_json : \n', main_json, '\nInvidual_jsons_arr : \n', individual_jsons_arr)

    # datasets_dir_path = tar_unpack()

    # aktualizowanie loggera (pod kątem poprawności nazw plików do sprawdzenia)
    check_datasets_names_and_extensions('datasets', main_json)
    csv_dataframes = load_multiple_csv_to_dataframes('datasets')
    i = 0
    for dataframe in csv_dataframes:
        check_column_names(dataframe, individual_jsons_arr[i])
        i += 1


if __name__ == '__main__':
    clear_logger()
    logger_function()
    log = logging.getLogger(__name__)
    log.info("A tu dziala")
    main()


