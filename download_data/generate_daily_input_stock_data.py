import setting
from datetime import datetime
from util import fileutil as file_util
import os
import pandas as pd
from dateutil.relativedelta import relativedelta
INPUT_TARGET_DATA_YEAR_SPAN = 3

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

            target_date_time = datetime.strptime(target_date, '%Y%m%d')
            insert_date = target_date_time.strftime("%Y-%m-%d")
            # print(insert_date)

            insert_value = [[insert_date, searched_data.iloc[0]['OPEN'], searched_data.iloc[0]['HIGH'], searched_data.iloc[0]['LOW'], searched_data.iloc[0]['CLOSE'], searched_data.iloc[0]['Volume']]]
            _tmp_df = pd.DataFrame(data=insert_value, columns=['DATE', 'OPEN', 'HIGH','LOW', 'CLOSE','Volume'])
            symb_df = pd.concat([_tmp_df, symb_df], sort=True)

            symb_df = symb_df.loc[:, ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'Volume']]

            target_data_span = target_date_time - relativedelta(years=INPUT_TARGET_DATA_YEAR_SPAN)

            symb_df['DATE'] = pd.to_datetime(symb_df['DATE'])
            symb_df.index = symb_df['DATE']
            target_data = symb_df[symb_df.index > target_data_span]

            # print(symb_df.info)
            save_file_path = os.path.join(setting.get_generated_input_target_stock_data_dir(), symb + '.csv')
            file_util.write_csv_without_index(target_data, save_file_path)

        generate_tracking_file(target_date)
        print('Generating input target stock data end.')
    else:
        print('No target download CSV file exists. file=' + target_download_csv_file_path)

def generate_tracking_file(target_date):
    file_util.write_file(setting.get_generated_stock_data_date_track_file(), target_date)

def main(target_date):
    generate_input_stock_data(target_date)

if __name__ == '__main__':
    target_date = datetime.now().strftime("%Y%m%d")
    # target_date = '20200603'
    main(target_date)