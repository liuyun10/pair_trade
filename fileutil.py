import shutil,os,glob
import pandas as pd

FILE_ENCODING='shift_jis'
def clean_target_dir(target_dir):

    if os.path.exists(target_dir):
        print('Cleaning the target dir:'+target_dir)
        shutil.rmtree(target_dir)

    os.makedirs(target_dir)

def create_target_dir(target_dir):

    if not os.path.exists(target_dir):
        print('Creating the target dir:'+target_dir)
        os.makedirs(target_dir)

def read_csv(file_full_path):
    return pd.read_csv(file_full_path, encoding=FILE_ENCODING)

def write_csv(data, file_full_path):
    data.to_csv(file_full_path, encoding=FILE_ENCODING)


def getAllTargetSymbols(input_data_dir):
    symbols = []
    file_list = sorted(glob.glob(input_data_dir + '\*.csv'))
    for file in file_list:
        path, ext = os.path.splitext(os.path.basename(file))
        symbols.append(path)
    return symbols

def is_file_exists(fullpath):
    return os.path.isfile(fullpath)