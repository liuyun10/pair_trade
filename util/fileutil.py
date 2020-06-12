import shutil,os,glob
import pandas as pd
import setting

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

def write_csv_without_index_header(data, file_full_path):
    data.to_csv(file_full_path, encoding=FILE_ENCODING, header=False, index=False)

def write_csv_without_index(data, file_full_path):
    data.to_csv(file_full_path, encoding=FILE_ENCODING, header=True, index=False)

def getAllTargetSymbols(input_data_dir):
    symbols = []
    file_list = sorted(glob.glob(input_data_dir + '\*.csv'))
    ignore_list = getIgnoreSymbolList()

    for file in file_list:
        path, ext = os.path.splitext(os.path.basename(file))
        if path not in ignore_list:
            symbols.append(path)
    return symbols

def is_file_exists(fullpath):
    return os.path.isfile(fullpath)

def write_file(fullpath, content):
    with open(fullpath, mode='w') as f:
        f.write(content)

def read_text_file(fullpath):
    with open(fullpath, mode='r') as f:
        l = f.readlines()
    return l

def getIgnoreSymbolList():
    file1 = open(setting.get_ignore_file_full_path(), 'r')
    result_list = []

    for line in file1.readlines():
        result_list.append(line.rstrip('\n'))
    return result_list

if __name__ == '__main__':
    print(getAllTargetSymbols(setting.get_input_test_data_dir()))
