import pandas as pd
import numpy as np
import glob, copy, os.path, time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from operator import itemgetter

pd.set_option('display.max_columns', None)

data_dir='G:\Stock\TradeStation\Price-data'
report_dir='result'
corr_result_file_name='corr.csv'
report_file_name='report'

### Const ###
FILE_ENCODING='shift_jis'

MEAN_WINDOW=75
# the threshold of corrb
CORR_THRE_SHOLD_THREE_MONTH=0.9
CORR_THRE_SHOLD_ONE_YEAR=0.9

def create_pairs_dataframe(data_dir, symbol1, symbol2):
    print("Importing CSV data...")
    # print("Constructing dual matrix for s% and s%" % (symbol1, symbol2))

    sym1 = pd.read_csv(os.path.join(data_dir, symbol1+'.csv'), encoding=FILE_ENCODING)
    sym2 = pd.read_csv(os.path.join(data_dir, symbol2 + '.csv'), encoding=FILE_ENCODING)

    sym1.rename(columns={'日付': 'DATE', 'OPEN': 'OPEN' + symbol1, 'CLOSE': 'CLOSE_' + symbol1}, inplace=True)
    sym2.rename(columns={'日付': 'DATE', 'OPEN': 'OPEN' + symbol2, 'CLOSE': 'CLOSE_' + symbol2}, inplace=True)

    pairs = pd.merge(sym1, sym2, on='DATE', how='left')
    pairs['DATE'] = pd.to_datetime(pairs['DATE'])
    pairs.index = pairs['DATE']

    pairs = pairs.drop(['HIGH_x','HIGH_y'], axis=1)
    pairs = pairs.dropna()

    return pairs

def check_corr(pairs, symbol1, symbol2):

    # Check the corr of pairs with 3 month data
    three_month_ago = datetime.today() - relativedelta(months=3)
    three_month_data = pairs[pairs.index] > three_month_ago
    s1 = pd.Series(three_month_data['CLOSE_'+symbol1])
    s2 = pd.Series(three_month_data['CLOSE_' + symbol2])
    res1 = s1.corr(s2)
    # print('%s - %s corr(three month)= %f' % (symbol1, symbol2, res1))

    # Check the corr of pairs with 3 month data
    one_year_ago = datetime.today() - relativedelta(years=1)
    one_year_data = pairs[pairs.index] > one_year_ago
    s1 = pd.Series(one_year_data['CLOSE_' + symbol1])
    s2 = pd.Series(one_year_data['CLOSE_' + symbol2])
    res2 = s1.corr(s2)
    # print('%s - %s corr(three month)= %f' % (symbol1, symbol2, res2))

    return res1, res2

def calculate_spread_zscore(pairs, symbol1, symbol2):

    # pairs['saya_minus'] = pairs['CLOSE_'+ symbol1] - pairs['CLOSE_'+symbol2]
    pairs['saya_divide'] = pairs['CLOSE_'+ symbol1] / pairs['CLOSE_'+symbol2]

    pairs['saya_divide_mean'] = (pd.Series(pairs['saya_divide'])).rolling(window=MEAN_WINDOW, center=False).mean()
    pairs['saya_divide_std'] = (pd.Series(pairs['saya_divide'])).rolling(window=MEAN_WINDOW, center=False).std(ddof=0)
    pairs['saya_divide_sigma'] = (pairs['saya_divide'] - pairs['saya_divide_mean']) / pairs['saya_divide_std']

    # _pairs = pairs.shift(1)

    return pairs

def print_chart(pairs, symbol1, symbol2):

    plt.title('Graph '+ symbol1 + '_' + symbol2)
    plt.xlabel('DATE')
    plt.ylabel('Y-Axis')

    x = pairs.index

    y1 = pairs['saya_divide_sigma']
    plt.plot(x, y1, label='sigma')

    y2= pairs['saya_divide_mean']
    plt.plot(x, y2, label='saya_mean')

    xmin, xmax = min(x), max(x)
    plt.hlines(2, xmin, xmax, color='red', linestyle='dashed', label='SIGMA=2', linewidth=0.5)
    plt.hlines(-2, xmin, xmax, color='red', linestyle='dashed', label='SIGMA=-2', linewidth=0.5)
    plt.hlines(0, xmin, xmax, color='blue', linestyle='dashed', label='ZERO LINE', linewidth=0.5)

    plt.legend()
    plt.show()

def output_report():

    timestr = time.strftime("%Y%m%d-%H%M%S")
    report_file = os.path.join(data_dir, report_dir, corr_result_file_name + '_' + timestr + '.xlsx')

    corr_df = pd.read_csv(os.path.join(data_dir, report_dir, corr_result_file_name), encoding=FILE_ENCODING)
    corr_df_new = corr_df.copy(deep=True)

    OPEN_A_list=[]
    CLOSE_A_list=[]
    OPEN_B_list = []
    CLOSE_B_list = []
    SIGMA=[]

    with pd.ExcelWriter(report_file) as writer:
        for index, row in corr_df.iterrows():
            # print('row.SYM_A:'+str(int(row.SYM_A)))
            symblA = str(int(row.SYM_A))
            symblB = str(int(row.SYM_B))
            try:
                _file = os.path.join(data_dir, report_dir, symblA + '_' + symblB + '.csv')
                _df = pd.read_csv(_file, encoding=FILE_ENCODING)

                OPEN_A_list.append(_df['OPEN_' + symblA][0])
                CLOSE_A_list.append(_df['CLOSE_' + symblA][0])
                OPEN_B_list.append(_df['OPEN_' + symblB][0])
                CLOSE_B_list.append(_df['CLOSE_' + symblB][0])
                SIGMA.append(_df['saya_divide_sigma'][0])

                path, ext = os.path.splitext(os.path.basename(_file))
                _df.to_excel(writer, sheet_name=path)

            except FileNotFoundError:
                OPEN_A_list.append(0)
                CLOSE_A_list.append(0)
                OPEN_B_list.append(0)
                CLOSE_B_list.append(0)
                SIGMA.append(0)
                continue

        corr_df_new = corr_df_new.assign(OPEN_A=OPEN_A_list, CLOSE_A=CLOSE_A_list, OPEN_B=OPEN_B_list,
                                         CLOSE_B=CLOSE_B_list, SIGMA=SIGMA)
        _df.to_excel(writer, sheet_name=path)

    writer.save()
    writer.close()

if __name__ == '__main__':
    print('maint start')

    symbols = []
    file_list = glob.glob(data_dir + '\*.csv')

    for file in file_list:
        path, ext = os.path.splitext(os.path.basename(file))
        symbols.append(path)

    symbols_corr_list=[]
    symbol_check_dict={}

    for symb1 in symbols:
        for symb2 in symbols:
            if (symb1 == symb2 or (symb1 + symb2) in symbol_check_dict or (symb2 + symb1) in symbol_check_dict):
                continue

            _pairs = create_pairs_dataframe(data_dir, symb1, symb2)
            corr1, corr2 = check_corr(_pairs, symb1, symb2)
            # print('%s - %s 3M:%f 1Y:%f' % (symb1, symb2, corr1, corr2))

            symbols_corr_list.append([symb1, symb2, corr1, corr2])
            symbol_check_dict[symb1 + symb2] =''

            if (corr1 < CORR_THRE_SHOLD_THREE_MONTH or corr2 < CORR_THRE_SHOLD_ONE_YEAR): continue

            _pairs = calculate_spread_zscore(_pairs, symb1, symb2)
            _pairs = _pairs.sort_values('DATE', ascending=False)
            _pairs.to_csv(os.path.join(data_dir, report_dir, symb1 + '_' + symb2 + '.csv'), encoding=FILE_ENCODING)

    print(symbols_corr_list)
    corr_data=sorted(symbols_corr_list, key=itemgetter(2), reverse=True) # sort by 3 month corr
    corr_data=pd.DataFrame(columns=['SYM_A', 'SYM_B', 'CORR_3M', 'CORR_1Y'], data=corr_data)
    corr_data.to_csv(os.path.join(data_dir, report_dir, corr_result_file_name), encoding=FILE_ENCODING)

    output_report()

    #print chart
    # pairs_one_year = pairs[pairs.index > (datetime.today() - relativedelta(years=1))]
    #print_chart(pairs_one_year, symbolA, symbolB)






