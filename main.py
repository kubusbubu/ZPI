from tools import logger_function, tar_unpack, get_json_files, create_tar_file, \
    load_multiple_csv_to_dataframes, clear_logger
from comparing import Comparing, check_datasets_names_and_extensions
import logging


def main():
    # create test .tar file
    create_tar_file('datasets', 'output.tar')

    # open json dda files
    main_json, individual_jsons_arr = get_json_files()

    # unpack tar file
    datasets_dir_path = tar_unpack()

    # print(datasets_dir_path)

    # load datasets to a list of pandas dataframes
    csv_dataframes, filenames = load_multiple_csv_to_dataframes(datasets_dir_path)

    # check if datasets names and extensions are valid
    check_datasets_names_and_extensions(main_json, datasets_dir_path)

    for i, dataframe in enumerate(csv_dataframes):
        shard_object = Comparing(individual_jsons_arr[i], dataframe, filenames[i])

        # check if column names in each dataset are valid
        shard_object.check_column_names()

        # check if each row in each dataset is valid type
        shard_object.check_dataframe_types()


if __name__ == '__main__':
    # clear logging file
    clear_logger()

    # init logger
    logger_function()
    log = logging.getLogger(__name__)

    # run
    main()

    with open('log.log', 'r') as log_file:
        for line in log_file:
            if line.strip():
                log.warning(f"No errors detected")
