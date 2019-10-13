import configparser
from sqlalchemy import create_engine
import pymysql
import pandas as pd
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# engine = create_engine("mysql://scott:tiger@hostname/dbname",
#                                     encoding='latin1', echo=True)
engine = create_engine('mysql://root:b00377837@localhost/mydbname',
                       encoding='utf8', echo=False)
def get_stock_mysql_config():
    cf = {}
    config = configparser.ConfigParser()
    config.read('mysql.config')

    cf['database'] = config.get('stock_db', 'database')
    cf['host'] = config.get('stock_db', 'host')
    cf['user'] = config.get('stock_db', 'user')
    cf['pwd'] = config.get('stock_db', 'pwd')
    return cf

from unittest import TestCase

df = pd.DataFrame({'columns':[1,2,3],'columns2':['a','b','c']})
print(df)
df.to_sql('test', con=engine, if_exists='append')
# sqlcf = get_stock_mysql_config()
# print(sqlcf)
# conns = pymysql.connect(host=sqlcf['host'], user=sqlcf['user'], db=sqlcf['database'], password=sqlcf['pwd'])
# with conns.cursor() as cursor:
#     sql = 'select * from db1_test;'
#     cursor.execute(sql)
#     print(cursor.fetchall())
