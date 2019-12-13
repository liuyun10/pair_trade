import openpyxl,sys

file_name = 'G:\\Stock\\pairs_trade\\pair_trade\\stock_data\\master\\pair_trade.xlsm'
sheet_name = '取引履歴'
def main(targetYM):
    workbook = openpyxl.load_workbook(file_name, data_only=True)
    sheet = workbook[sheet_name]
    record_list = []
    for i in range(4, sheet.max_row + 1, 2):
        record = TradeRecord()
        year = sheet.cell(row=i, column=27).value
        if (year is None):
            continue
        record.ym = str(year) + str(sheet.cell(row = i, column =28).value)
        if (targetYM != record.ym):
            continue
        record.sellCode = str(sheet.cell(row = i, column= 6).value)
        record.buyCode = str(sheet.cell(row = i + 1, column= 6).value)
        record_list.append(record)
    for record in record_list:
        record.printAll()

class TradeRecord:
    id = ""
    ym = ""
    sellCode = ""
    buyCode = ""
    name = ""
    def printAll(self):
        print(self.ym + self.sellCode + self.buyCode)

if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 2):
        print('Please input target date! YYYYMM')
        sys.exit()
    main(args[1])