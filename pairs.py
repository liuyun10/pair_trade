import pandas as pd
import numpy as np
import glob, copy, os.path, time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from operator import itemgetter
import shutil,numpy
from time import gmtime, strftime

pd.set_option('display.max_columns', None)

data_dir='G:\Stock\pairs_trade\pair_trade\stock_data'
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
    # print("Importing CSV data...")
    # print("Constructing dual matrix for s% and s%" % (symbol1, symbol2))

    sym1 = pd.read_csv(os.path.join(data_dir, symbol1+'.csv'), encoding=FILE_ENCODING)
    sym2 = pd.read_csv(os.path.join(data_dir, symbol2 + '.csv'), encoding=FILE_ENCODING)

    sym1.rename(columns={'OPEN': 'OPEN_' + symbol1, 'CLOSE': 'CLOSE_' + symbol1}, inplace=True)
    sym2.rename(columns={'OPEN': 'OPEN_' + symbol2, 'CLOSE': 'CLOSE_' + symbol2}, inplace=True)

    pairs = pd.merge(sym1, sym2, on='DATE', how='left')
    pairs['DATE'] = pd.to_datetime(pairs['DATE'])
    pairs.index = pairs['DATE']

    pairs = pairs.drop(['DATE','HIGH_x','HIGH_y','LOW_x','LOW_y','Volume_x','Volume_y'], axis=1)
    pairs = pairs.dropna()

    return pairs

def check_corr(pairs, symbol1, symbol2):

    # Check the corr of pairs with 3 month data
    three_month_ago = datetime.today() - relativedelta(months=3)
    three_month_data = pairs[pairs.index > three_month_ago]
    s1 = pd.Series(three_month_data['CLOSE_'+symbol1])
    s2 = pd.Series(three_month_data['CLOSE_' + symbol2])
    res1 = s1.corr(s2)
    # print('%s - %s corr(three month)= %f' % (symbol1, symbol2, res1))

    # Check the corr of pairs with 3 month data
    one_year_ago = datetime.today() - relativedelta(years=1)
    one_year_data = pairs[pairs.index > one_year_ago]
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
    pairs['deviation_rate(%)'] = round((pairs['saya_divide'] - pairs['saya_divide_mean']) / pairs['saya_divide'] *100,2)

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

    print('Output Report Processing...')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    report_file = os.path.join(data_dir, report_dir, corr_result_file_name + '_' + timestr + '.xlsx')

    corr_df = pd.read_csv(os.path.join(data_dir, report_dir, corr_result_file_name), encoding=FILE_ENCODING)
    corr_df_new = corr_df.copy(deep=True)

    OPEN_A_list=[]
    CLOSE_A_list=[]
    OPEN_B_list = []
    CLOSE_B_list = []
    SIGMA=[]
    DEV_RATE=[]

    with pd.ExcelWriter(report_file) as writer:
        for index, row in corr_df.iterrows():
            # print('row.SYM_A:'+str(int(row.SYM_A)))
            symblA = str(int(row.SYM_A))
            symblB = str(int(row.SYM_B))
            #print('symblA=%s symblB=%s' % (symblA,symblB))
            try:
                _file = os.path.join(data_dir, report_dir, symblA + '_' + symblB + '.csv')
                _df = pd.read_csv(_file, encoding=FILE_ENCODING)

                OPEN_A_list.append(_df['OPEN_' + symblA][0])
                CLOSE_A_list.append(_df['CLOSE_' + symblA][0])
                OPEN_B_list.append(_df['OPEN_' + symblB][0])
                CLOSE_B_list.append(_df['CLOSE_' + symblB][0])
                SIGMA.append(_df['saya_divide_sigma'][0])
                DEV_RATE.append(_df['deviation_rate(%)'][0])

                #print(_df)
                signal_generate(_df, symblA, symblB)

                path, ext = os.path.splitext(os.path.basename(_file))
                #_df.to_excel(writer, sheet_name=path)

            except FileNotFoundError:
                OPEN_A_list.append(0)
                CLOSE_A_list.append(0)
                OPEN_B_list.append(0)
                CLOSE_B_list.append(0)
                SIGMA.append(0)
                DEV_RATE.append(0)
                continue

        corr_df_new = corr_df_new.assign(OPEN_A=OPEN_A_list, CLOSE_A=CLOSE_A_list, OPEN_B=OPEN_B_list,
                                         CLOSE_B=CLOSE_B_list, SIGMA=SIGMA,DEV_RATE=DEV_RATE)
        #print(corr_df_new)
        corr_df_new['ABS_SIGMA'] = np.abs(corr_df_new['SIGMA'])
        corr_df_new = corr_df_new.sort_values('ABS_SIGMA', ascending=False)
        corr_df_new.to_csv(os.path.join(data_dir, report_dir, 'corr_result.csv'), encoding=FILE_ENCODING)

        corr_df_new.to_excel(writer, sheet_name='CORR')

    writer.save()
    writer.close()

    print('Output Report Process end!')

def clean_result_dir():

    result_dir = os.path.join(data_dir, report_dir)
    if os.path.exists(result_dir):
        print('Cleaning the result dir:'+report_dir)
        shutil.rmtree(result_dir)

    os.makedirs(result_dir)

def signal_generate(pairs, symbol_Axis, symbol_Pair, z_entry_threshold=1.8, z_exit_threshold1=0, entry_max_days=25, stop_loss_rate=0.05):

    pairs = pairs.sort_values('DATE', ascending=True)
    pairs['DATE'] = pd.to_datetime(pairs['DATE'])
    pairs.index = pairs['DATE']

    pairs['axis_A_long']= (pairs['saya_divide_sigma'] <= -z_entry_threshold) *1.0
    pairs['axis_A_short'] = (pairs['saya_divide_sigma'] >= z_entry_threshold) * 1.0
    pairs['axis_A_exit_long'] = (pairs['saya_divide_sigma'] >= -1 * z_exit_threshold1) * 1.0
    pairs['axis_A_exit_short'] = (pairs['saya_divide_sigma'] <= z_exit_threshold1) * 1.0

    #pairs = pairs.sort_values('DATE', ascending=True)
    #print(pairs)

    position ={}
    portfolio_list = []
    last_row_index=''
    haveUnsettledPostion=False

    for index, row in pairs.iterrows():

        if numpy.isnan(row['saya_divide_sigma']):
            last_row_index = index
            continue

        OPEN_CAT=''
        CLOSE_CAT=''

        if haveUnsettledPostion:
            #print(position)
            _cat = position['OPEN_CAT']

            open_days = int((index-position['OPEN_DATE']) / np.timedelta64(1, 'D'))
            if 'BUY' == _cat and pairs.at[last_row_index, 'axis_A_exit_long'] == 1:
                CLOSE_CAT = 'CLOSE_BUY'
            elif 'SELL' == _cat and pairs.at[last_row_index, 'axis_A_exit_short'] ==1:
                CLOSE_CAT = 'CLOSE_SELL'
            elif open_days > entry_max_days: # Stop Loss
                CLOSE_CAT = 'SL_MAX_DAY_OVER'

            if len(CLOSE_CAT) > 0:
                axisClosePrice = row['OPEN_'+ symbol_Axis]
                pairClosePrice = row['OPEN_' + symbol_Pair]

                position['CLOSE_DATE'] = index

                position['OPEN_DAYS'] = open_days
                position['CLOSE_CAT'] = CLOSE_CAT
                position['AXIS_SYMB_CLOSE_PRI'] = axisClosePrice
                position['PAIR_SYMB_CLOSE_PRI'] = pairClosePrice

                axis_lot_size = position['AXIS_SYMB_LOT']
                pair_lot_size = position['PAIR_SYMB_LOT']
                position['AXIS_CLOSE_MOUNT'] = axisClosePrice*axis_lot_size
                position['PAIR_CLOSE_MOUNT'] = pairClosePrice * pair_lot_size

                axisOpenPrice = position['AXIS_SYMB_OPEN_PRI']
                pairOpenPrice = position['PAIR_SYMB_OPEN_PRI']

                haveUnsettledPostion = False

                if  CLOSE_CAT == 'CLOSE_BUY' or (CLOSE_CAT == 'SL_MAX_DAY_OVER' and 'BUY'==_cat):
                    total = (axisClosePrice - axisOpenPrice) * axis_lot_size + (pairOpenPrice - pairClosePrice) * pair_lot_size
                elif CLOSE_CAT == 'CLOSE_SELL' or (CLOSE_CAT == 'SL_MAX_DAY_OVER' and 'SELL'==_cat):
                    total = (axisOpenPrice - axisClosePrice) * axis_lot_size + (pairClosePrice - pairOpenPrice) * pair_lot_size

                position['TOTAL'] = total
                trade_commission = get_trade_commission(axisOpenPrice,pairOpenPrice, axis_lot_size,pair_lot_size)
                position['COMMISSION_N'] = trade_commission
                credit_commission=get_credit_commission(axisOpenPrice,pairOpenPrice,axis_lot_size,pair_lot_size,open_days)
                position['COMMISSION_CREDIT'] = credit_commission

                profit = total - trade_commission - credit_commission
                position['PROFIT'] = profit

                pl = round(profit / (position['AXIS_OPEN_MOUNT'] + position['PAIR_OPEN_MOUNT'])*100,2)
                position['PL'] = pl

                #print(portfolio_list)
                portfolio_list.append(position)

        else:

            if pairs.at[last_row_index, 'axis_A_long'] == 1:
                OPEN_CAT = 'BUY' # BUY AXIS COMBOL

            elif pairs.at[last_row_index, 'axis_A_short'] == 1:
                OPEN_CAT = 'SELL'

            if len(OPEN_CAT) > 0:

                sigma = round(pairs.at[last_row_index, 'saya_divide_sigma'],2)
                haveUnsettledPostion = True
                axisOpenPrice = row['OPEN_' + symbol_Axis]
                pairOpenPrice = row['OPEN_' + symbol_Pair]
                axis_lot_size,pair_lot_size,lot_size_diff = get_lot_size(axisOpenPrice, pairOpenPrice)

                position = {'AXIS_SYMBOL': symbol_Axis, 'PAIR_SYMBOL': symbol_Pair, 'OPEN_DATE': index,
                            'SIGMA':sigma, 'OPEN_CAT':OPEN_CAT,"AXIS_SYMB_OPEN_PRI":axisOpenPrice,
                            'AXIS_SYMB_LOT':axis_lot_size, 'AXIS_OPEN_MOUNT':axisOpenPrice*axis_lot_size,
                            'PAIR_SYMB_OPEN_PRI':pairOpenPrice,'PAIR_SYMB_LOT':pair_lot_size,
                            'PAIR_OPEN_MOUNT':pairOpenPrice*pair_lot_size,'LOT_DIFF(%)':lot_size_diff,}

        last_row_index = index

    pd_portfolio_list = pd.DataFrame(portfolio_list)
    pd_portfolio_list.to_csv(os.path.join(data_dir, report_dir, symbol_Axis + '_' + symbol_Pair + 'portfolio.csv'), encoding=FILE_ENCODING)

def get_lot_size(axisPrice, pairPrice):
    min_lot_size = 100
    maxMount = 500000
    mixMount = 100000

    unit_axis_lot_size = min_lot_size
    unit_pair_lot_size = min_lot_size

    if axisPrice > pairPrice:
        ratio = round(axisPrice / pairPrice)
        unit_pair_lot_size = min_lot_size * ratio

    else:
        ratio = round(pairPrice / axisPrice)
        unit_axis_lot_size = min_lot_size * ratio

    axis_lot_size = unit_axis_lot_size
    pair_lot_size = unit_pair_lot_size

    while True:

        if axis_lot_size * axisPrice < maxMount and pair_lot_size * pairPrice < maxMount:
            axis_lot_size = axis_lot_size + unit_axis_lot_size
            pair_lot_size = pair_lot_size + unit_pair_lot_size

        else:
            if axis_lot_size != unit_axis_lot_size or pair_lot_size != unit_pair_lot_size:
                axis_lot_size = axis_lot_size - unit_axis_lot_size
                pair_lot_size = pair_lot_size - unit_pair_lot_size
            break
    lot_diff = np.abs(
        round((axis_lot_size * axisPrice - pair_lot_size * pairPrice) / (axis_lot_size * axisPrice) * 100, 2))

    return axis_lot_size, pair_lot_size, lot_diff

def get_trade_commission(axisPrice, pairPrice, axis_lot_size, pair_lot_size):

    consumtion_tax_ration = 0.1
    axia_total = axisPrice * axis_lot_size

    if axia_total > 500000:
        axis_commission = 350
    else:
        axis_commission =180

    pair_total = pairPrice * pair_lot_size
    if pair_total > 500000:
        pair_commission = 350
    else:
        pair_commission =180

    axis_commission = axis_commission*2*(1+consumtion_tax_ration)
    pair_commission = pair_commission*2*(1+consumtion_tax_ration)

    return axis_commission + pair_commission

def get_credit_commission(axisPrice, pairPrice, axis_lot_size, pair_lot_size, open_days):

    credit_rate=0.03

    axis_comm = axisPrice * axis_lot_size * credit_rate /365 * open_days
    pair_comm = pairPrice * pair_lot_size * credit_rate / 365 * open_days

    total = round(axis_comm + pair_comm)
    return total

if __name__ == '__main__':
    print('maint start ' + strftime("%Y-%m-%d %H:%M:%S"))

    clean_result_dir()

    symbols = []
    file_list = sorted(glob.glob(data_dir + '\*.csv'))

    for file in file_list:
        path, ext = os.path.splitext(os.path.basename(file))
        symbols.append(path)

    symbols_corr_list=[]
    symbol_check_dict={}
    print('Total symbols size:' + str(len(symbols)))
    index1=0
    for symb1 in symbols:
        index1=index1+1
        # index2=0
        print('Processing {0}/{1} {2}...'.format(index1, len(symbols), symb1))
        for symb2 in symbols:
            # index2 =index2+1
            #  print('Processing {0}/{1}/{2} {3}-{4}...'.format(index2,index1, len(symbols), symb1, symb2))
            if (symb1 == symb2 or (symb1 + symb2) in symbol_check_dict or (symb2 + symb1) in symbol_check_dict):
                continue

            _pairs = create_pairs_dataframe(data_dir, symb1, symb2)
            corr1, corr2 = check_corr(_pairs, symb1, symb2)
            # print('%s - %s 3M:%f 1Y:%f' % (symb1, symb2, corr1, corr2))

            symbols_corr_list.append([symb1, symb2, corr1, corr2])
            symbol_check_dict[symb1 + symb2] =''

            if (corr1 < CORR_THRE_SHOLD_THREE_MONTH or corr2 < CORR_THRE_SHOLD_ONE_YEAR): continue

            _pairs = _pairs.sort_values('DATE', ascending=True)
            _pairs = calculate_spread_zscore(_pairs, symb1, symb2)
            _pairs = _pairs.sort_values('DATE', ascending=False)
            _pairs.to_csv(os.path.join(data_dir, report_dir, symb1 + '_' + symb2 + '.csv'), encoding=FILE_ENCODING)

    #print(symbols_corr_list)
    corr_data=sorted(symbols_corr_list, key=itemgetter(2), reverse=True) # sort by 3 month corr
    corr_data=pd.DataFrame(columns=['SYM_A', 'SYM_B', 'CORR_3M', 'CORR_1Y'], data=corr_data)
    corr_data.to_csv(os.path.join(data_dir, report_dir, corr_result_file_name), encoding=FILE_ENCODING)


    output_report()
    print('main end!'+ strftime("%Y-%m-%d %H:%M:%S"))

    # signal_generate(_pairs, '9064','9505')

    #print chart
    # pairs_one_year = pairs[pairs.index > (datetime.today() - relativedelta(years=1))]
    #print_chart(pairs_one_year, symbolA, symbolB)






