# Copyright (C) 2019, Xudong Pan
from download_data import download_data_main
from scrape_data import Scrape_fiscal_data as get_fiscal, Scrape_gyakunipo as get_gyakunipo
from analysis import position_history_analysis, dryrun_analysis, watching_list_data_analysis
from datetime import datetime
import sys
import pair_trade,setting
from time import strftime
import logging
from util.log_helper import LogHelper

def main(argv):

    # Setup logger
    LogHelper.setup(log_path='{}/sayatori_trade.log'.format(setting.output_log_file_path), log_level=logging.INFO)
    _logger = logging.getLogger(__name__)

    start_time = datetime.now()
    print('Sayatori main start ' + strftime("%Y-%m-%d %H:%M:%S"))
    _logger.info('Sayatori main start ' + strftime("%Y-%m-%d %H:%M:%S"))

    # download stock price data and generate target input data
    download_data_main.main()
    # download fiscal date of target stocks
    get_fiscal.main()
    # download gakkunipo data of target stocks
    get_gyakunipo.main()

    # Pair trade main process
    pair_trade.main(argv)

    # caculate the data of open position and history trade
    position_history_analysis.main()
    # caculate the data of open position and history trade for dry-run
    dryrun_analysis.main()
    # watching list get
    watching_list_data_analysis.main()

    process_time = datetime.now() - start_time
    print('Sayatori main end!' + strftime("%Y-%m-%d %H:%M:%S"))
    print('Sayatori main time cost:{0}'.format(process_time))
    _logger.info('Sayatori main end!' + strftime("%Y-%m-%d %H:%M:%S"))
    _logger.info('Sayatori main time cost:{0}'.format(process_time))

if __name__ == '__main__':
    main(sys.argv)