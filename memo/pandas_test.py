import pandas as pd
import numpy as np
from datetime import datetime

def create_df():
    date_rng = pd.date_range(start='1/1/2019', end='4/30/2019', freq='D')
    # print(date_rng)
    # print(type(date_rng[0]))
    df = pd.DataFrame(date_rng, columns=['date'])
    df['open'] = np.random.randint(0, 100, size=(len(date_rng)))
    df['close'] = np.random.randint(0, 100, size=(len(date_rng)))
    # print(df.head(15))

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    # df.drop(['date'], axis=1, inplace=True)
    print(df.head())
    # df.info()
    print(df.describe())
    # print(df.tail())

    return df

def select_pd(df):
    print(df.loc['2019-01-01': '2019-01-31'])
    # print(df.loc['1/1/2019': '1/31/2019'])
    print(df.loc['2019-01-01': '2019-01-31', 'open'])
    print(df.iloc[1:5, 0:2])  # print date open close
    print(df.iloc[1:5, 1:])  # pring close
    print(df.iloc[:, 1:])  # print all rows
    print(df.iloc[0:5])  # print all columns
    print(df.close[0:3])  # print 0-3 rows only close column
    print(df[['close', 'open']][0:3])  # print 0-3 rows only close column
    # print(df[df['close'] > 50])
    # print(df.open.mean())
    # print(df[(df['close'] > 50) & (df['open'] > df.open.mean())])
    print(df)
    # print(df.sort_values(by='close')[:5])
    print(df.sort_values(by='close', ascending=False)[:5])
    df.dropna()
    df.dropna(how='all')
    df.fillna(df.close.mean(), inplace=True)


def change_df(df):
    print(df.close[:5])
    df1 = df.close.pct_change()[:5]
    print(df1)
    # df1 = df1.dropna()
    # df1 = df1.dropna(how='all')
    df1.fillna(0, inplace=True)
    # print(df1)

    change_ratio = df.close.pct_change()
    # print(change_ratio.tail())
    change_ratio = np.round(change_ratio * 100, 2)
    # print(change_ratio.tail())
    # print(type(change_ratio))

    df['change_ratio'] = change_ratio
    print(df.tail())
    # df.change_ratio.hist(bins=80)

    cats = pd.qcut(np.abs(df.change_ratio), 10)
    print(cats.value_counts())

def concat_df(df):
    # print(df)

    date_rng2 = pd.date_range(start='1/2/2019', end='4/30/2019', freq='D')
    # print(date_rng)
    df2 = pd.DataFrame(date_rng2, columns=['date'])
    df2['vloume'] = np.random.randint(10, 10000, size=(len(date_rng2)))
    df2['date'] = pd.to_datetime(df2['date'])
    df2 = df2.set_index('date')
    # print(df2)

    # new_pd = pd.concat([df, df2], axis=1)
    # print(new_pd)
    app_df1 = df[df.close > 50]
    print(app_df1)
    print(len(app_df1))

    app_df2 = df[df.open > 50]
    print(app_df2)
    print(len(app_df2))

    app_df12 = app_df1.append(app_df2)
    print(app_df12)
    print(len(app_df12))

    # print(df[df.close > 50].append(df[df.open > 60]))

def df_other(df):

    print(df)
    df['change_ratio']  = np.round(df.close.pct_change() * 100, 2)
    df['positive'] = np.where(df.change_ratio > 0, 1, 0)
    # print(df.index)
    df['date_week'] = df.index.weekday
    print(df)
    print(df.dtypes)

    # print(type(df.close))
    # print(df.close)
    # print(type(df['close']))
    # print(df['close'])

    xt = pd.crosstab(df.date_week, df.positive)
    print(xt)
    xt_pct = xt.div(xt.sum(1).astype(float), axis=0)
    print(xt_pct)

    piv_df = df.pivot_table(['positive'], index=['date_week'])
    print(piv_df)

    gro_df = df.groupby(['date_week', 'positive'])['positive'].count()
    print(gro_df)

def main():
    print("main start")
    df = create_df()
    # select_pd(df)
    # change_df(df)
    # concat_df(df)
    df_other(df)

if __name__ == '__main__':
    main()