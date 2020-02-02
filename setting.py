import os

input_data_dir='G:\Stock\pairs_trade\pair_trade\stock_data'
#input_data_dir='G:\Stock\pairs_trade\pair_trade\stock_data\\test'

RESULT_FILE_DIR='result'
MASTER_FILE_DIR='master'
FILE_ENCODING='shift_jis'

corr_result_file_name='corr.csv'
report_file_name='report'

SAYA_MEAN_WINDOW=75

# the threshold of corr
CORR_THRE_SHOLD_THREE_MONTH=0.8
CORR_THRE_SHOLD_ONE_YEAR=0.8

# the threshold of coint
# p-value
COINT_MAX_VAL_THREE_MONTH=0.6
COINT_MAX_VAL_ONE_YEAR=0.4

#For back test (max open oprice diff)
MAX_OPEN_PRICE_DIFF=10

def get_input_data_dir():
    return input_data_dir

def get_result_dir():
    return  os.path.join(get_input_data_dir(), RESULT_FILE_DIR)

def get_master_dir():
    return os.path.join(get_input_data_dir(), MASTER_FILE_DIR)

def get_master_file_dir():
    return  os.path.join(get_input_data_dir(), MASTER_FILE_DIR,'master.csv')

def get_currenty_report_file():
    return  os.path.join(get_input_data_dir(), MASTER_FILE_DIR,'corr_result.csv')