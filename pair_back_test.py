import fileutil as ft
import setting as setting
import pairs as pairs_util
import tradeutil as tu
import os
import pandas as pd
from time import strftime
from dateutil.relativedelta import relativedelta
from datetime import datetime

input_test_data_dir = os.path.join(setting.get_input_data_dir(), 'back_test')

caculated_csv_dir = os.path.join(input_test_data_dir, 'pre_caculate')
portfolio_csv_dir = os.path.join(input_test_data_dir, 'portfolio')
backtest_report_dir = os.path.join(input_test_data_dir, 'backtest_report')
backtest_report_each_day_dir = os.path.join(backtest_report_dir, 'each_day')

start_date = '2018-10-06'
end_date = '2018-10-09'

capital = 5000000
max_pair_size = 5 # 10 symbol
per_lot_capital = 1000000

SAYA_MEAN_WINDOW = 75
# the threshold of corr
CORR_THRE_SHOLD_THREE_MONTH=0.9
CORR_THRE_SHOLD_ONE_YEAR=0.9
# the threshold of coint p-value
COINT_MAX_VAL=0.4
# For back test (max open price diff)
MAX_OPEN_PRICE_DIFF=5 # 5%

z_entry_threshold=2
#z_exit_threshold=0
entry_max_days=15
stop_loss_rate=0.025 # total 5%
stop_profit_rate=0.025 # total 5%
refer_history_profit_span = 1 # 1 year, 2 years, or all data

# mode create(clear all then create) insert(insert data in existing file  Default)
def generate_caculated_data_csv(symbols, caculated_csv_path=caculated_csv_dir, startdate=None,
                                enddate = None, mode='insert'):
    symbol_check_dict = {}

    if (mode == 'create'):
        ft.clean_target_dir(caculated_csv_path)
    else:
        ft.create_target_dir(caculated_csv_path)

    index1 = 0
    for symb1 in symbols:
        index1 = index1 + 1
        print('Processing {0}/{1} {2}...'.format(index1, len(symbols), symb1))
        for symb2 in symbols:

            if (symb1 == symb2 or (symb1 + symb2) in symbol_check_dict or (symb2 + symb1) in symbol_check_dict):
                continue
            symbol_check_dict[symb1 + symb2] = ''

            _pairs = pairs_util.create_pairs_dataframe(setting.get_input_data_dir(), symb1, symb2)

            if startdate is not None:
                start_date = datetime.datetime.strftime(startdate, '%Y-%m-%d')
                _pairs = _pairs[_pairs.index >= start_date]
            if enddate is not None:
                end_date = datetime.datetime.strftime(enddate, '%Y-%m-%d')
                _pairs = _pairs[_pairs.index <= end_date]
            #_pairs = _pairs[(_pairs.index >= startdate) & (_pairs.index <= enddate)]

            result_write_csv = os.path.join(caculated_csv_path, symb1 + '_' + symb2 + '.csv')
            _pairs = _pairs.sort_values('DATE', ascending=True)
            _pairs = pairs_util.calculate_spread_zscore(_pairs, symb1, symb2)

            if ft.is_file_exists(result_write_csv):
                csv_pairs = ft.read_csv(result_write_csv)
                csv_pairs['DATE'] = pd.to_datetime(csv_pairs['DATE'])
                csv_pairs = csv_pairs.sort_values('DATE', ascending=True)
                csv_pairs.index = csv_pairs['DATE']

                last_row_date = csv_pairs.tail(1).index
                # print ('last_row_date {0}'.format(last_row_date))

                _pairs = _pairs.combine_first(csv_pairs)
                result_write_csv = os.path.join(caculated_csv_path, symb1 + '_' + symb2 + '.csv')

                _pairs = _pairs.loc[:,
                         ['OPEN_'+ symb1, 'CLOSE_'+ symb1, 'OPEN_'+ symb2, 'CLOSE_'+ symb2,
                          'saya_divide','saya_divide_mean','saya_divide_std','saya_divide_sigma',
                          'deviation_rate(%)','CORR_3M','COINT_3M','CORR_1Y','COINT_1Y']]

                _pairs = _pairs.sort_values('DATE', ascending=False)
                set_corr_and_coint(_pairs, symb1, symb2, last_row_date)
                ft.write_csv(_pairs, result_write_csv)

            else:
                _pairs = _pairs.sort_values('DATE', ascending=False)
                set_corr_and_coint(_pairs, symb1, symb2)
                ft.write_csv(_pairs, result_write_csv)

def set_corr_and_coint(paris, symbol1, symbol2, start_index = None):

    last_row_date = paris.tail(1).index

    for index, row in paris.iterrows():

        if start_index is not None and index <= start_index:
            break

        # set for 3 month
        three_month_ago = index - relativedelta(months=3)
        if three_month_ago > last_row_date:
            three_month_data = paris[(paris.index < index) & (paris.index > three_month_ago)]

            # set corr
            s1 = pd.Series(three_month_data['CLOSE_' + symbol1])
            s2 = pd.Series(three_month_data['CLOSE_' + symbol2])
            paris.loc[index, 'CORR_3M'] = tu.check_correlation(s1,s2)

            # set coint
            coint_3m = tu.check_cointegration_common(three_month_data, symbol1, symbol2)
            paris.loc[index, 'COINT_3M'] = coint_3m[1]
        else:
            paris.loc[index, 'CORR_3M'] = 0
            paris.loc[index, 'COINT_3M'] = 0

        # set for 1 year
        one_year_ago = index - relativedelta(years=1)
        if one_year_ago > last_row_date:
            one_year_data = paris[(paris.index < index) & (paris.index > one_year_ago)]

            # set corr
            s1 = pd.Series(one_year_data['CLOSE_' + symbol1])
            s2 = pd.Series(one_year_data['CLOSE_' + symbol2])
            paris.loc[index, 'CORR_1Y'] = tu.check_correlation(s1, s2)

            # set coint
            coint_1y = tu.check_cointegration_common(one_year_data, symbol1, symbol2)
            paris.loc[index, 'COINT_1Y'] = coint_1y[1]
        else:
            paris.loc[index, 'CORR_1Y'] = 0
            paris.loc[index, 'COINT_1Y'] = 0

def generate_portfolio_csv_file(caculated_csv_path = caculated_csv_dir, portfolio_csv_path=portfolio_csv_dir):
    print('generate_portfolio_csv_file start ' + strftime("%Y-%m-%d %H:%M:%S"))
    ft.clean_target_dir(portfolio_csv_path)

    file_name_list = ft.getAllTargetSymbols(caculated_csv_path)
    index1 = 0
    for file_name in file_name_list:
        index1 = index1 + 1
        print('Processing {0}/{1}...'.format(index1, len(file_name_list)))
        _temp = file_name.split('_')
        pairs_data = ft.read_csv(os.path.join(caculated_csv_path, file_name + '.csv'))
        pairs_util.signal_generate(pairs_data, _temp[0], _temp[1], portfolio_csv_path)

    print('generate_portfolio_csv_file end ' + strftime("%Y-%m-%d %H:%M:%S"))

def generate_backtest_report(caculated_csv_path = caculated_csv_dir, portfolio_csv_path=portfolio_csv_dir,
                             backtest_report_path = backtest_report_dir, startdate=start_date, enddate=end_date):
    print('generate_backtest_report start ' + strftime("%Y-%m-%d %H:%M:%S"))
    print('start_date: {0} enddate: {1}'.format(startdate, enddate))

    ft.clean_target_dir(backtest_report_dir)
    ft.clean_target_dir(backtest_report_each_day_dir)

    start_date =datetime.strptime(startdate, '%Y-%m-%d')
    end_date = datetime.strptime(enddate, '%Y-%m-%d')

    file_name_list = ft.getAllTargetSymbols(caculated_csv_path)

    for target_date in tu.date_span(start_date, end_date):
        print(target_date)

        weekno = target_date.weekday()
        if weekno < 5:
            generate_day_report(target_date, file_name_list)

    print('generate_backtest_report end ' + strftime("%Y-%m-%d %H:%M:%S"))

def generate_day_report(target_date, file_name_list):

    day_report_file_name = os.path.join(backtest_report_each_day_dir, target_date.strftime("%Y-%m-%d") + '.csv')

    # temp_data = ft.read_csv(os.path.join(caculated_csv_dir, file_name_list[0] + '.csv'))
    # day_report_data = pd.DataFrame([], columns=temp_data.columns)
    day_report_data = pd.DataFrame()

    for file_name in file_name_list:

        _temp = file_name.split('_')
        symb1 = _temp[0]
        symb2 = _temp[1]

        pairs_data = ft.read_csv(os.path.join(caculated_csv_dir, file_name + '.csv'))
        pairs_data['DATE'] = pd.to_datetime(pairs_data['DATE'])
        pairs_data.index = pairs_data['DATE']
        search_data = pairs_data[target_date : target_date]
        if search_data.empty:
            # print('empty {0}'.format(target_date))
            return

        search_data1 = search_data.copy(deep=True)
        search_data1.rename(columns={'OPEN_'+ symb1: 'OPEN_A', 'CLOSE_'+ symb1: 'CLOSE_A',
                                                  'OPEN_'+ symb2: 'OPEN_B', 'CLOSE_'+ symb2: 'CLOSE_B'}, inplace=True)

        search_data1['SYM_A'] = symb1
        search_data1['SYM_B'] = symb2

        search_data1 = search_data1.loc[:,
                 ['SYM_A', 'OPEN_A', 'CLOSE_A', 'SYM_B', 'OPEN_B', 'CLOSE_B',
                  'saya_divide', 'saya_divide_mean', 'saya_divide_std', 'saya_divide_sigma',
                  'deviation_rate(%)', 'CORR_3M', 'COINT_3M', 'CORR_1Y', 'COINT_1Y']]

        if search_data1.at[target_date, 'CORR_3M'] < CORR_THRE_SHOLD_THREE_MONTH \
                or search_data.at[target_date, 'CORR_1Y'] < CORR_THRE_SHOLD_ONE_YEAR:
            continue

        if search_data1.at[target_date, 'COINT_3M'] > COINT_MAX_VAL \
            or search_data.at[target_date, 'COINT_1Y'] > COINT_MAX_VAL:
            continue

        day_report_data = day_report_data.append(search_data1)

    if not day_report_data.empty:
        ft.write_csv(day_report_data, day_report_file_name)

def main():

    start_time = datetime.now()
    print('main start ' + strftime("%Y-%m-%d %H:%M:%S"))

    symbols = ft.getAllTargetSymbols(input_test_data_dir)

    generate_caculated_data_csv(symbols)

    generate_portfolio_csv_file()

    generate_backtest_report()

    process_time = datetime.now() - start_time
    print('main end ' + strftime("%Y-%m-%d %H:%M:%S"))
    print('Time cost: {0}'.format(process_time))

if __name__ == '__main__':
    main()