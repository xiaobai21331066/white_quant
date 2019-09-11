import tushare as ts
from sqlalchemy import create_engine
import pandas as pd

ts.set_token('1f4aecee1853f8ed3d2bb79559025a997563bddad50008ecab9f93bb')
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# engine = create_engine("mysql://scott:tiger@hostname/dbname",
#                                     encoding='latin1', echo=True)
engine = create_engine('mysql://root:b00377837@localhost/mydbname',
                       encoding='utf8', echo=False)
favered_stocks = ['002797','000063','600816','002927','002143','002415','002236','002558','600643',
                  '600519','300104','000776','002680','000939','000802','300184']

favered_indexs = ['1A0001','2A01']
#stock_pool = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']
for stock in favered_stocks:
    print('stock:{}'.format(stock))
    result_df = ts.get_hist_data(stock)
    print(result_df.head())
    result_df.to_sql('daily', con=engine, if_exists='append')
