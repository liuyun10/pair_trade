import fileutil as file_util
import setting, os
import pandas as pd

def generate_list():

    symbols = file_util.getAllTargetSymbols(setting.get_input_data_dir())
    df = pd.DataFrame(data=symbols, columns=["CODE"])

    save_file = setting.get_target_stock_data_list_file_path()
    file_util.write_csv_without_index(df, save_file)

if __name__ == '__main__':
    generate_list()