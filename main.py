import csv
import tarfile
import json
import os
import glob
import logging


def log_init():
    logging.basicConfig(level=logging.INFO, filname="log.log", filemode="w")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logger.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_json_files():
    while True:
        folder_path = input("Enter dda folder path: ")
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


def get_dataset_names(main_json_marketdata, dataset_dir_path, json_dir_path):
    dataset_names = []
    for dataset in main_json_marketdata['datasets']:
        dataset_names.append(dataset['name' + '.csv'])

    dataset_names.sort()
    dataset_file_names = [f for f in os.listdir(dataset_dir_path) if os.path.isfile(os.path.join(dataset_dir_path, f))].sort()
    individual_json_file_names = [f for f in os.listdir(json_dir_path) if os.path.isfile(os.path.join(json_dir_path, f))].sort()

    for i in range(len(dataset_names)):
        if os.path.splitext(dataset_file_names[0])[0] == os.path.splitext(individual_json_file_names[0])[0] == os.path.splitext(dataset_names[0])[0]:
            print('ok')
        else:
            logger.warning("Wrong extensions")
    return dataset_names


def tar_handling():
    #unpacks tar file
    tar_file_path = input("Enter path to tar file:")
    output_dir = 'tar_output_dir'
    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extractall(output_dir)
    return output_dir


def check_csv(csv):
    #looks for errors in individual csv files
    pass


def main():
    log_init()
    get_json_files()
    datasets_dir_path = tar_handling()
    get_dataset_names()


if __name__ == '__main__':
    main()

