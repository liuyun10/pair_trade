import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import statsmodels.tsa.stattools as ts

def get_lot_size(axisPrice, pairPrice):

    maxMount = 1100000
    # mixMount = 1000000
    min_lot_size = 100

    if axisPrice <= 0 or pairPrice <= 0:
        return 1,1,100
    elif axisPrice * min_lot_size > maxMount or pairPrice * min_lot_size  > maxMount:
        return 1,1,100

    axis_lot_size = min_lot_size
    pair_lot_size = min_lot_size
    lot_dict = {}

    try:
        if axisPrice > pairPrice:
            axis_lot_size = math.floor(maxMount / axisPrice / min_lot_size) * min_lot_size
            # print("axis_lot_size {0}".format(axis_lot_size))

            while True:
                lot_diff = np.abs(round((axis_lot_size * axisPrice - pair_lot_size * pairPrice) / (axis_lot_size * axisPrice) * 100,2))
                lot_dict.setdefault(pair_lot_size, lot_diff)
                if pair_lot_size * pairPrice > maxMount:
                    break
                else:
                    pair_lot_size = pair_lot_size + min_lot_size

            pair_lot_size = min(lot_dict, key=lot_dict.get)  # get the key of min in all list
            lot_diff = lot_dict[pair_lot_size]
            # print(pair_lot_size)
        else:
            pair_lot_size = math.floor(maxMount / pairPrice / min_lot_size) * min_lot_size
            # print("pair_lot_size {0}".format(pair_lot_size))

            while True:
                lot_diff = np.abs(round((pair_lot_size * pairPrice - axis_lot_size * axisPrice) / (pair_lot_size * pairPrice) * 100,2))
                lot_dict.setdefault(axis_lot_size, lot_diff)
                if axis_lot_size * axisPrice > maxMount:
                    break
                else:
                    axis_lot_size = axis_lot_size + min_lot_size

            axis_lot_size = min(lot_dict, key=lot_dict.get)  # get the key of min in all list
            lot_diff = lot_dict[axis_lot_size]
            # print(axis_lot_size)

    except:
        lot_diff = 1

    return axis_lot_size, pair_lot_size, lot_diff

#取引手数料
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

def get_trade_commission2(price, mount):

    tax_rate = 0.1
    totalMount = price * mount

    if totalMount > 500000:
        commission = 350
    else:
        commission =180

    return commission * 2 * (1 + tax_rate)

#for sell position
def get_credit_commission_for_sell_position(price, mount, open_days):
    rate = 0.011
    return price * mount * rate / 365 * open_days

#for buy position
def get_credit_commission_for_buy_position(price, mount, open_days):
    rate = 0.028
    return price * mount * rate / 365 * open_days

#信用取引手数料
def get_credit_commission(axisPrice, pairPrice, axis_lot_size, pair_lot_size, open_days):

    credit_rate=0.03
    axis_comm = axisPrice * axis_lot_size * credit_rate /365 * open_days
    pair_comm = pairPrice * pair_lot_size * credit_rate / 365 * open_days

    total = round(axis_comm + pair_comm)
    return total

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

def addMasterInfo(corr_df, master_df):

    stockA_name_list = []
    stockB_name_list = []
    stockA_industry_list = []
    stockB_industry_list = []

    master_df.index = master_df['SYMBL']

    for index2, row in corr_df.iterrows():
        symblA = int(row.SYM_A)
        symblB = int(row.SYM_B)

        # print("symblA:{0} symblB:{1}".format(symblA,symblB))

        stockA_name_list.append(master_df[master_df.index == symblA].at[symblA, 'NAME'])
        stockB_name_list.append(master_df[master_df.index == symblB].at[symblB, 'NAME'])
        stockA_industry_list.append(master_df[master_df.index == symblA].at[symblA, 'INDUSTRY'])
        stockB_industry_list.append(master_df[master_df.index == symblB].at[symblB, 'INDUSTRY'])

    corr_df = corr_df.assign(SYM_A_NAME=stockA_name_list, SYM_B_NAME=stockB_name_list, SYM_A_INDUSTRY=stockA_industry_list, SYM_B_INDUSTRY=stockB_industry_list)
    corr_df = corr_df.loc[:,['SYM_A', 'SYM_A_NAME', 'SYM_A_INDUSTRY','SYM_B', 'SYM_B_NAME', 'SYM_B_INDUSTRY','CORR_3M','CORR_1Y','COINT_3M','COINT_1Y']]

    return corr_df

def check_corr(pairs, symbol1, symbol2):

    # Check the corr of pairs with 3 month data
    three_month_ago = datetime.today() - relativedelta(months=3)
    three_month_data = pairs[pairs.index > three_month_ago]
    s1 = pd.Series(three_month_data['CLOSE_'+symbol1])
    s2 = pd.Series(three_month_data['CLOSE_' + symbol2])
    res_3m = check_correlation(s1, s2)
    # print('%s - %s corr(three month)= %f' % (symbol1, symbol2, res1))

    # Check the corr of pairs with 1 year data
    one_year_ago = datetime.today() - relativedelta(years=1)
    one_year_data = pairs[pairs.index > one_year_ago]
    s1 = pd.Series(one_year_data['CLOSE_' + symbol1])
    s2 = pd.Series(one_year_data['CLOSE_' + symbol2])
    res_1y = check_correlation(s1, s2)
    # print('%s - %s corr(three month)= %f' % (symbol1, symbol2, res2))
    return res_3m, res_1y

def check_correlation (series1, series2):
    return series1.corr(series2)

def check_cointegration(pairs, symbol1, symbol2):
    # print "Computing Cointegration..."
    three_month_ago = datetime.today() - relativedelta(months=3)
    three_month_data = pairs[pairs.index > three_month_ago]
    coin_result1 = check_cointegration_common(three_month_data, symbol1, symbol2)

    one_year_ago = datetime.today() - relativedelta(years=1)
    one_year_data = pairs[pairs.index > one_year_ago]
    coin_result2 = check_cointegration_common(one_year_data, symbol1, symbol2)

    #Confidence Level chosen as 0.05 (5%)
    return coin_result1[1], coin_result2[1]

def check_cointegration_common (pairs, symbol1, symbol2):

    try:
        x = ts.coint(pairs['CLOSE_'+symbol1], pairs['CLOSE_'+symbol2] )
        return x
    except ValueError:
        print('check_cointegration_common Error. values:')
        print(pairs['CLOSE_'+symbol1])
        print(pairs['CLOSE_' + symbol2])
    return 1.0

def date_span(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

if __name__ == '__main__':
    result=get_lot_size(1401,2000)
    print(result)
