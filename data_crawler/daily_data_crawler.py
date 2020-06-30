
from pymongo import UpdateOne
from data_crawler.database import DB_CONN
from datetime import datetime as dt
from data_crawler import stock_util
from util import fileutil as file_util, tradeutil as tu

"""
Dowload Daily Stock data then save to database
"""

class DailyCrawler:
    def __init__(self):
        self.daily = DB_CONN['daily']
        # self.daily_hfq = DB_CONN['daily_hfq']

    def crawl_index(self, begin_date=None, end_date=None):
        """
        Download Nikke 225 Index data .
        Nikke 225 Index is for createing open trade date and compare profit rate

        :param begin_date: download start date
        :param end_date: download end date
        """

        # set Nikke Index code
        index_codes = ['1001']

        now = dt.now().strftime('%Y-%m-%d')
        if begin_date is None:
            begin_date = now
        if end_date is None:
            end_date = now

        # for code in index_codes:
            # 抓取一个指数的在时间区间的数据
            # df_daily = ts.get_k_data(code, index=True, start=begin_date, end=end_date)
            # 保存数据
            # self.save_data(code, df_daily, self.daily, {'index': True})

    def save_data(self, code, df_daily, collection, extra_fields=None):
        """
        Save downloaded data to MongoDB

        :param code: symbol
        :param df_daily: daily data DataFrame
        :param collection: table
        :param extra_fields:
        """
        update_requests = []

        for df_index in df_daily.index:
            # convert one row data to dict
            doc = dict(df_daily.loc[df_index])
            doc['CODE'] = str(code)

            if extra_fields is not None:
                doc.update(extra_fields)

            print(doc)

            # db.daily.createIndex({'code':1,'date':1,'index':1})
            update_requests.append(
                UpdateOne(
                    {'CODE': doc['CODE'], 'DATE': doc['DATE']},
                    {'$set': doc},
                    upsert=True)
            )

        if len(update_requests) > 0:
            update_result = collection.bulk_write(update_requests, ordered=False)
            print('Save data to MongoDB，Code： %s, Insert：%4d, Update：%4d' %
                  (code, update_result.upserted_count, update_result.modified_count),
                  flush=True)

    def crawl_stock(self, begin_date=None, end_date=None):
        """
        Download stock data then save to MongoDB

        :param begin_date: download start date
        :param end_date: download end date
        """
        now = dt.now().strftime('%Y-%m-%d')
        if begin_date is None:
            begin_date = now
        else:
            begin_date = dt.strptime(begin_date, '%Y-%m-%d')

        if end_date is None:
            end_date = now
        else:
            end_date = dt.strptime(end_date, '%Y-%m-%d')

        codes = stock_util.get_all_codes()

        for target_date in tu.date_span(begin_date, end_date):
            # print(target_date)

            target_date_ymd = target_date.strftime("%Y%m%d")
            weekno = dt.strptime(target_date_ymd, '%Y%m%d').weekday()
            if weekno >=5:
                continue

            for code in codes:
                # 抓取不复权的价格
                df_daily = stock_util.get_daily_stock_data(code, target_date_ymd)
                if df_daily is not None:
                    self.save_data(code, df_daily, self.daily)

# Main
if __name__ == '__main__':
    dc = DailyCrawler()

    # dc.crawl_index('2015-01-01', '2015-12-31')
    dc.crawl_stock('2020-05-21', '2020-06-23')
