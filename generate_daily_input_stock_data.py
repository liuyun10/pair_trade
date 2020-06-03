import setting
from datetime import datetime
import fileutil as file_util
import os
import pandas as pd

def generate_input_stock_data(target_date):

    target_download_csv_file_path = setting.get_target_download_csv_file_path(target_date)

    if (file_util.is_file_exists(target_download_csv_file_path)):
        print('Generating input target stock data start.')
        target_stock_data_list = file_util.read_csv(setting.get_target_stock_data_list_file_path())
        # print(target_stock_data_list)
        # print(target_stock_data_list['CODE'][0])

        download_stock_data =file_util.read_csv(target_download_csv_file_path)
        columns=['DATE', 'CODE', 'KBN', 'OPEN', 'HIGH', 'LOW', 'CLOSE','Volume']
        download_stock_data.columns = columns
        # print(download_stock_data)
        # print(download_stock_data.dtypes)

        for index, data_row in target_stock_data_list.iterrows():
            symb = str(data_row['CODE'])
            # print('symb:'+ symb)

            data_csv_file = os.path.join(setting.get_org_all_stock_data_file_dir(), symb + '.csv')
            symb_df = file_util.read_csv(data_csv_file)
            # symb_df['DATE'] = symb_df.to_datetime(symb_df['DATE'])
            newest_date = symb_df['DATE'][0]
            # print('newest_date：' + newest_date)

            searched_data = download_stock_data[download_stock_data['CODE'] == data_row['CODE']]

            # print(searched_data['HIGH'])
            # print(searched_data.iloc[0]['HIGH'])

            tdatetime = datetime.strptime(target_date, '%Y%m%d')
            insert_date = tdatetime.strftime("%Y-%m-%d")
            # print(insert_date)

            insert_value = [[insert_date, searched_data.iloc[0]['OPEN'], searched_data.iloc[0]['HIGH'], searched_data.iloc[0]['LOW'], searched_data.iloc[0]['CLOSE'], searched_data.iloc[0]['Volume']]]
            _tmp_df = pd.DataFrame(data=insert_value, columns=['DATE', 'OPEN', 'HIGH','LOW', 'CLOSE','Volume'])
            symb_df = pd.concat([_tmp_df, symb_df], sort=True)

            symb_df = symb_df.loc[:, ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'Volume']]
            symb_df = symb_df[:-1]
            # print(symb_df.info)
            save_file_path = os.path.join(setting.get_generated_input_target_stock_data_dir(), symb + '.csv')
            file_util.write_csv_without_index(symb_df, save_file_path)

        print('Generating input target stock data end.')
    else:
        print('No target download CSV file exists. file=' + target_download_csv_file_path)

if __name__ == '__main__':
    target_date = datetime.now().strftime("%Y%m%d")
    target_date = '20200602'
    generate_input_stock_data(target_date)