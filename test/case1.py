from rqalpha.api import *
from rqalpha import run_func
import pandas as pd
import talib
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool

from rqalpha.api import *

    get_
pool = Pool()
pool.map_async()

def weight_decide(res):
    alist = []
    for i in range(len(res)):
        alist.append((res[i], 2 * (len(res) - i) / (len(res) * (1 + len(res)))))
    return alist

def get_data(stock, data_index):
    res = history_bars(stock, 30, '1d', data_index)
    return np.array(res)

def before_trading(context):
    fina
    context.stock_list = index_component('')

def handle_bar(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        res = pd.Series(talib.TRANGE(get_data(stock, 'high'), get_data(stock, 'low'), get_data(stock, 'close')))
        try:
            if context.price_list[stock].iloc[-1] - context.price_list[stock].iloc[-2] < -0.95 * res.iloc[-2]:
                order_target_percent(stock, 0)
        except:
            if stock not in context.price_list.columns:
                order_target_percent(stock, 0)
    alias = weight_decide(context.chosen)
    for stock in alias:
        order_target_percent(stock[0], stock[1])

def init(context):

