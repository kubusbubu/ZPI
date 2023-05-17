from tools import logger_function, tar_unpack, date_format_standardization, get_json_files, create_tar_file, \
    load_multiple_csv_to_dataframes, clear_logger
from comparing import date_format_check, check_datasets_names_and_extensions, check_column_names,  check_dataframe_types
import logging


def main():
    # create test .tar file
    create_tar_file('datasets', 'output.tar')

    # open json dda files
    main_json, individual_jsons_arr = get_json_files()

    # unpack tar file
    datasets_dir_path = tar_unpack()

    # check if datasets names and extensions are valid
    check_datasets_names_and_extensions(datasets_dir_path, main_json)

    # load datasets to a list of pandas dataframes
    csv_dataframes = load_multiple_csv_to_dataframes(datasets_dir_path)

    i = 0
    for dataframe in csv_dataframes:
        # check if column names in each dataset are valid
        check_column_names(dataframe, individual_jsons_arr[i])

        # check if each row in each dataset is valid type
        check_dataframe_types(dataframe, individual_jsons_arr[i])
        i += 1


if __name__ == '__main__':
    # clear logging file
    clear_logger()

    # init logger
    logger_function()
    log = logging.getLogger(__name__)

    # run
    main()


