import fileutil as file_util
import setting, os
import pandas as pd

def generate_list():

    symbols = file_util.getAllTargetSymbols(setting.get_input_data_dir())
    df = pd.DataFrame(symbols)

    save_file = os.path.join(setting.get_input_data_dir(), 'stock_data', 'target_stock_list.csv')
    file_util.write_csv_without_index_header(df, save_file)

if __name__ == '__main__':
    generate_list()