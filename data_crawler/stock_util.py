from util import fileutil as file_util
import setting
from download_data import data_download
def get_all_codes():
    """
    Get all target stock codes

    """
    # return DB_CONN.basic.distinct('code')
    target_stock_data_list = file_util.read_csv(setting.get_target_stock_data_list_file_path())
    # print(target_stock_data_list)
    return target_stock_data_list['CODE'].tolist()

def get_daily_stock_data(code, target_ymd):
    """
    Get target daily stock date by code and date(YYYYmmDD)

    """
    target_download_csv_file_path = setting.get_target_download_csv_file_path(target_ymd)
    if (not file_util.is_file_exists(target_download_csv_file_path)):
        data_download.main(target_ymd)

    if (not file_util.is_file_exists(target_download_csv_file_path)):
        print("No target data")
        return None
    else:
        download_daily_stock_data = file_util.read_csv(target_download_csv_file_path)
        # columns=['DATE', 'CODE', 'KBN', 'OPEN', 'HIGH', 'LOW', 'CLOSE','Volume']
        download_daily_stock_data.columns = ['DATE', 'CODE', 'KBN', 'OPEN', 'HIGH', 'LOW', 'CLOSE','Volume']
        searched_data = download_daily_stock_data[download_daily_stock_data['CODE'] == code]
        searched_data['Volume'] = searched_data['Volume'].astype(float)
        searched_data = searched_data.drop('KBN', 1)

        return searched_data

if __name__ == '__main__':
    codes = get_all_codes()
    print(codes)