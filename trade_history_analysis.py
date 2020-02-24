import openpyxl,sys
import setting, os, pairs
import pandas as pd
import pair_back_test
import fileutil as ft
import argparse
excel_file_full_path = setting.get_trade_excel_full_path()
output_csv_file_full_path = os.path.join(setting.get_master_dir(),  "trade_history.csv")

##################################################################################################
# Default parameters                                                                              #
##################################################################################################
# Other exit condition
EXIT_MAX_OPEN_DAYS=15
# Stop Loss
EXIT_stop_loss_rate=-0.025 # total 2.5%
# Stop Profit
EXIT_stop_profit_rate=0.025 # total 2.5%
# Zero Loss
# 0: exit positon when totalreturn(yesterday) > 0 and totalreturn(today) < totalreturn(yesterday)
# 1:  exit positon when totalreturn(yesterday) > 0.01 and totalreturn(today) < totalreturn(yesterday)
EXIT_ZERO_LOSS_CONDITION = None

EXIT_threshold_when_plus_sigma = None
EXIT_threshold_when_minus_sigma = None
##################################################################################################
# Define parameters                                                                              #
##################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--trade_data_path", type=str, default="./stock_data/trade/",
                    help="Path to trade stock price data")
# parser.add_argument("--output_dir", type=str, default="./data/output/", help="Path to output directory.")
parser.add_argument("--backtest_start_ym", type=str, default=None,
                    help="Start date YM(close) of backtest. e.g. 201911")
parser.add_argument("--backtest_end_ym", type=str, default=None,
                    help="End date YM(close) of backtest. e.g. 202111")
parser.add_argument("--zero_loss_strategy_type", default=EXIT_ZERO_LOSS_CONDITION, type=str, choices=["None", "0", "1", "2"],
                    help="Type of zeor loss strategy used.")
parser.add_argument("--exit_threshold_when plus_sigma", default=EXIT_threshold_when_plus_sigma, type=str,
                    help="Exit threshold value to be tested (in units 'number of SD from mean').")
parser.add_argument("--exit_threshold_when minux_sigma", default=EXIT_threshold_when_minus_sigma, type=str,
                    help="Exit threshold value to be tested (in units 'number of SD from mean').")
parser.add_argument("--stop_profit_limit", default=EXIT_stop_profit_rate, type=float,
                    help="Position will exit if total 2 pairs profit exceeded this loss limit.")
parser.add_argument("--stop_loss_limit", default=EXIT_stop_loss_rate, type=float,
                    help="Position will exit if total 2 pairs loss exceeded this loss limit.")
parser.add_argument("--loss_limit_max_days", default=EXIT_MAX_OPEN_DAYS, type=str,
                    help="Position will exit if loss exceeded this max openning day limit.")
config = parser.parse_args()

def main():
    output_trade_history_to_csv()
    cacluate_trade_result()

def cacluate_trade_result():
    trade_history_data = ft.read_csv(output_csv_file_full_path)
    print(trade_history_data)
    #print(config)



def output_trade_history_to_csv():

    workbook = openpyxl.load_workbook(excel_file_full_path, data_only=True)
    sheet = workbook[setting.sheet_name_history]

    data_list = []

    for i in range(4, sheet.max_row + 1, 2):
        record = TradeHistoryRecord()
        year = sheet.cell(row=i, column=27).value
        if (year is None):
            continue

        record.year = str(year)
        record.month = str(sheet.cell(row = i, column =28).value)

        record.open_date= str(sheet.cell(row = i, column= 4).value).replace(' 00:00:00','')
        record.close_date = str(sheet.cell(row=i, column=21).value).replace(' 00:00:00','')

        record.sellCode = str(sheet.cell(row = i, column= 6).value)
        record.sellCodeName = str(sheet.cell(row=i, column=7).value)
        record.sellOpenPrice = str(sheet.cell(row = i, column= 8).value)
        record.sellMount = str(sheet.cell(row=i, column=9).value)
        record.sellClosePrice = str(sheet.cell(row=i, column=12).value)
        record.sellTradeFee = str(sheet.cell(row = i, column= 13).value)
        record.sellInterestFee = str(sheet.cell(row=i, column=14).value)
        record.sellOtherFee = str(sheet.cell(row=i, column=15).value)

        record.buyCode = str(sheet.cell(row = i + 1, column= 6).value)
        record.buyCodeName = str(sheet.cell(row= i + 1, column=7).value)
        record.buyOpenPrice = str(sheet.cell(row = i + 1, column= 8).value)
        record.buyMount = str(sheet.cell(row=i + 1, column=9).value)
        record.buyClosePrice = str(sheet.cell(row=i + 1, column=12).value)
        record.buyTradeFee = str(sheet.cell(row = i + 1, column= 13).value)
        record.buyInterestFee = str(sheet.cell(row=i + 1, column=14).value)
        record.buyOtherFee = str(sheet.cell(row=i + 1, column=15).value)

        record.totolReturn = str(sheet.cell(row=i, column=18).value)
        record.totolReturnRate = str(sheet.cell(row=i, column=19).value)
        record.open_days = str(sheet.cell(row=i, column=22).value)
        record.result = str(sheet.cell(row=i, column=23).value)

        data_list.append(convert_record_to_list(record))

    pd_data = pd.DataFrame(data_list, columns=record_column())
    ft.write_csv_without_index(pd_data, output_csv_file_full_path)

def convert_record_to_list(data):
    row_list = []
    row_list.append(data.year)
    row_list.append(data.month)

    row_list.append(data.open_date)
    row_list.append(data.close_date)

    row_list.append(data.sellCode)
    row_list.append(data.sellCodeName)
    row_list.append(data.sellOpenPrice)
    row_list.append(data.sellMount)
    row_list.append(data.sellClosePrice)
    row_list.append(data.sellTradeFee)
    row_list.append(data.sellInterestFee)
    row_list.append(data.sellOtherFee)

    row_list.append(data.buyCode)
    row_list.append(data.buyCodeName)
    row_list.append(data.buyOpenPrice)
    row_list.append(data.buyMount)
    row_list.append(data.buyClosePrice)
    row_list.append(data.buyTradeFee)
    row_list.append(data.buyInterestFee)
    row_list.append(data.buyOtherFee)

    row_list.append(data.totolReturn)
    row_list.append(data.totolReturnRate)
    row_list.append(data.open_days)
    row_list.append(data.result)
    return row_list

def record_column():
    columns = ['YEAR', 'MONTH', 'open_date', 'close_date',
               'sellCode', 'sellCodeName', 'sellOpenPrice', 'sellMount', 'sellClosePrice', 'sellTradeFee', 'sellInterestFee', 'sellOtherFee',
               'buyCode', 'buyCodeName', 'buyOpenPrice', 'buyMount', 'buyClosePrice', 'buyTradeFee', 'buyInterestFee', 'buyOtherFee',
               'totolReturn','totolReturnRate', 'open_days','result']
    return columns

class TradeHistoryRecord:
    id = ""
    open_date = ""
    close_date = ""
    sellCode = ""
    sellCodeName = ""
    sellOpenPrice = ""
    sellClosePrice = ""
    sellMount = ""
    sellTradeFee = ""
    sellInterestFee = ""
    sellOtherFee = ""
    buyCode = ""
    buyCodeName=""
    buyOpenPrice = ""
    buyClosePrice = ""
    buyMount=""
    buyTradeFee = ""
    buyInterestFee = ""
    buyOtherFee = ""
    name = ""
    kbn = ""
    totolReturn = ""
    totolReturnRate = ""
    open_days = ""
    year=""
    month=""
    result = ""

    def printAll(self):
        print(self.year + self.month + self.sellCode + self.buyCode)

if __name__ == '__main__':
    args = sys.argv
    main()