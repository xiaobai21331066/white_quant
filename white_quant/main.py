from rqalpha import run_func
from rqalpha.data.base_data_source import BaseDataSource

import sys
import os
import pickle
import pathlib
import pandas as pd
from multiprocessing import Pool, freeze_support

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from single_stock_strategies.golden_cross_strategy import GoldenCrossSingleStrategy
from single_stock_strategies.macd_strategy import MACDSingleStrategy

from config import config_utils

class SingleStockStrategyBest(object):

    def __init__(self, strategy_name=None, result_path=None):
        self.strategy_name=strategy_name
        self.result_path= pathlib.Path(result_path)

    def choose_strategy(self, stock_id, name='baseline_strategy'):
        print('choose strategy:{}'.format(name))
        if name == 'golden_cross':
            return GoldenCrossSingleStrategy().compose_user_func(stock_id)
        elif name == 'macd':
            return MACDSingleStrategy().compose_user_func(stock_id)
        return None

    def choose_stock_iterate(self):
        bd = BaseDataSource(os.path.join(os.path.expanduser('~'), '.rqalpha', 'bundle'))
        all_instruments = bd.get_all_instruments()
        all_instruments = pd.DataFrame([item.__dict__ for item in all_instruments])
        all_instruments = all_instruments[all_instruments['exchange'].apply(lambda x: x in ('XSHE', 'XSHG'))]
        all_instruments = all_instruments[all_instruments['type'] == 'CS']
        all_instruments = all_instruments[all_instruments['board_type'].apply(lambda x: x in ('MainBoard', 'SMEBoard', 'GEM'))]
        all_instruments = all_instruments[all_instruments['status'] == 'Active']
        for stock_id in all_instruments['order_book_id'].values[0:3]:
            print('choose stock:{}'.format(stock_id))
            yield stock_id

    def compute_strategy(self, stock_id):
        # 您可以指定您要传递的参数
        user_func = self.choose_strategy(stock_id, name=self.strategy_name)
        user_func['config'] = config_utils.parse_config('./config/config_20190909.yml')
        print('use strategy:{}'.format(stock_id))
        print('user_func:{}'.format(user_func))
        result = run_func(**user_func)
        base_path = self.result_path.joinpath(self.strategy_name)
        if not base_path.exists():
            base_path.mkdir(parents=True)
        result_path = base_path.joinpath(stock_id.split('.')[0] + '.pk')
        with result_path.open('wb') as f:
            pickle.dump(result, f)
        return stock_id

    def excute(self):
        print('__name__:{}',format(__name__))
        pool = Pool(3)
        try:
            result = pool.map_async(self.compute_strategy, self.choose_stock_iterate())
            print(result.get(7200))
        except Exception as e:
            print(e)
        pool.close()
        pool.join()
        print('finished compute all stocks.')

if __name__ == '__main__':
    freeze_support()
    SingleStockStrategyBest(strategy_name='macd', result_path='./result').excute()
