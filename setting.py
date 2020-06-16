import os
root_dir='G:\Stock\pairs_trade\pair_trade'

# root_data_dir = os.path.join(root_dir, 'stock_data')
# root_stock_data_dir = os.path.join(root_data_dir, 'stock_data') #download data file, generated input target data etc
# input_data_dir = os.path.join(root_dir, 'stock_data')
# input_data_dir_test=os.path.join(root_dir, 'stock_data','test')
# RESULT_FILE_DIR='result'
# MASTER_FILE_DIR='master'
# TRADE_FILE_DIR='trade'
# report_file_name='report'

#CONST
# the threshold of corr
CORR_THRE_SHOLD_THREE_MONTH=0.5
CORR_THRE_SHOLD_ONE_YEAR=0.85

# the threshold of coint
# p-value
COINT_MAX_VAL_THREE_MONTH=0.5
COINT_MAX_VAL_ONE_YEAR=0.1

#For back test (max open oprice diff)
MAX_OPEN_PRICE_DIFF=7

SAYA_MEAN_WINDOW=75

FILE_ENCODING='shift_jis'

#Result file name
corr_result_file_name='corr_result.csv'
watching_corr_result_file_name='watching_corr_result.csv'

#SHEET NAME
sheet_name_history = 'Trade History'

# Logging
output_log_file_path ='G:\Stock\pairs_trade\log'

def get_root_dir():
    return root_dir
def get_root_data_dir():
    return os.path.join(get_root_dir(), 'stock_data')

def get_trade_excel_full_path():
    return  os.path.join(get_root_dir(), 'pair_trade.xlsm')

def get_stock_data_dir():
    return os.path.join(get_root_data_dir(), 'stock_data')
def get_result_dir():
    return  os.path.join(get_root_data_dir(), 'result')
def get_master_dir():
    return os.path.join(get_root_data_dir(), 'master')
def get_watching_list_file_dir():
    return os.path.join(get_root_data_dir(), 'watching')

#trade analysis
def get_trade_dir():
    return os.path.join(get_root_data_dir(), 'trade')
def get_trade_open_dir():
    return os.path.join(get_trade_dir(), 'open')
def get_trade_history_analysis_dir():
    return os.path.join(get_trade_dir(), 'trade_history_analysis')
#master
def get_master_file_dir():
    return  os.path.join(get_master_dir(), 'master.csv')
def get_currenty_report_file():
    return  os.path.join(get_master_dir(), 'corr_result.csv')
def get_ignore_file_full_path():
    return  os.path.join(get_master_dir(), 'ignore_symbols.txt')

# dry-run
def get_dryrun_trade_dir():
    return os.path.join(get_trade_dir(), 'dry-run')
def get_dryrun_trade_open_dir():
    return os.path.join(get_dryrun_trade_dir(), 'open')
def get_dryrun_trade_history_dir():
    return os.path.join(get_dryrun_trade_dir(), 'history')

# stock data download, generate input data
def get_download_stock_file_dir():
    return os.path.join(get_stock_data_dir(), 'download_files')
def get_org_all_stock_data_file_dir():
    return os.path.join(get_stock_data_dir(),  'org_data')
def get_generated_input_target_stock_data_dir():
    return os.path.join(get_stock_data_dir(), 'input_data')
def get_target_stock_data_list_file_path():
    return os.path.join(get_stock_data_dir(),  'target_stock_list.csv')
def get_generated_stock_data_date_track_file():
    return os.path.join(get_stock_data_dir(), 'stock_data_last_update_date.txt')
def get_target_download_csv_file_path(target_date):
    return os.path.join(get_download_stock_file_dir(), target_date + '.csv')
# input data
def get_input_data_dir():
    return os.path.join(get_stock_data_dir(), 'input_data')
    #return get_root_data_dir()
def get_input_test_data_dir():
    return os.path.join(get_input_data_dir(), 'test')
