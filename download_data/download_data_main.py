from util import fileutil as file_util, tradeutil as tu
from download_data import data_download
from download_data import generate_daily_input_stock_data
from datetime import datetime
import setting
from time import strftime
from dateutil.relativedelta import relativedelta

def main():

    # target_date = '20200603'
    start_time = datetime.now()
    print('Input Target Stock Data Process....' + strftime("%Y-%m-%d %H:%M:%S"))

    last_update_date = file_util.read_text_file(setting.get_generated_stock_data_date_track_file())
    start_date = datetime.strptime(last_update_date[0], '%Y%m%d')
    start_date = start_date + relativedelta(days=1)
    end_date = datetime.now()

    for target_date in tu.date_span(start_date, end_date):
        # print(target_date)
        target_date_ymd = target_date.strftime("%Y%m%d")
        # print(target_date_ymd)
        data_download.main(target_date_ymd)
        generate_daily_input_stock_data.main(target_date_ymd)

    process_time = datetime.now() - start_time
    print('Input Target Stock Data Process end! '+ strftime("%Y-%m-%d %H:%M:%S"))
    print('Input Target Stock Data Process Time cost:{0}'.format(process_time))

if __name__ == '__main__':
    main()