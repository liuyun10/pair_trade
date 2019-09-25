import numpy as np
import math
import matplotlib.pyplot as plt

def get_lot_size(axisPrice, pairPrice):

    if axisPrice <= 0 or pairPrice <= 0:
        return 1,1,1

    maxMount = 1000000
    # mixMount = 1000000

    min_lot_size = 100
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

if __name__ == '__main__':
    result=get_lot_size(1401,2000)
    print(result)
