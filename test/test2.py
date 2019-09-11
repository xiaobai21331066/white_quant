# run_func_demo
from rqalpha.api import *
from rqalpha import run_func
import pandas as pd
from functools import wraps
from multiprocessing import freeze_support
import time
import abc

class SingleStrategyBase(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def compose_user_func(cls, stock_id):
        pass

class GoldenCrossSingleStrategy(SingleStrategyBase):

    golden_cross_config = {
      "base": {
        "start_date": "2019-03-01",
        "end_date": "2019-09-01",
        "benchmark": None,
        "accounts": {
            "stock": 100000
        }
      },
      "extra": {
        "log_level": "verbose",
      },
      "mod": {
        "sys_analyser": {
          "enabled": True,
          "plot": True
        }
      }
    }

    def compose_user_func(cls, stock_id):
        user_func = {'init': cls.golden_cross_init(stock_id),
                     'before_trading': cls.golden_cross_before_trading,
                     'handle_bar': cls.golden_cross_handle_bar,
                     'config': cls.golden_cross_config}
        return user_func

    @staticmethod
    def golden_cross_init(stock_id):
        """decorater"""
        print('call decorater: time{}', time.time())
        def add_stock(context):
            """add stock"""
            print('call add_stock: time{}', time.time())
            logger.info("init")
            # 是否已发送了order
            context.fired = False
            context.s1 = stock_id
            update_universe(context.s1)
            context.fired = False
        return add_stock

    # def user_init(func):
    #     """user_init"""
    #     print('call user_init: time{}', time.time())
    #     def decorater(stock_id):
    #         """decorater"""
    #         print('call decorater: time{}', time.time())
    #         @wraps(func)
    #         def add_stock(context):
    #             """add stock"""
    #             print('call add_stock: time{}', time.time())
    #             func(context)
    #             context.s1 = stock_id
    #             update_universe(context.s1)
    #             context.fired = False
    #         return add_stock
    #     return decorater
    #
    # @user_init
    # def golden_cross_init(context):
    #     logger.info("init")
    #     # 是否已发送了order
    #     context.fired = False

    @staticmethod
    def golden_cross_before_trading(context):
        pass

    @staticmethod
    def golden_cross_handle_bar(context, bar_dict):
        if not context.fired:
            # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
            order_percent(context.s1, 1)
            context.fired = True

from multiprocessing import Pool

class SingleStockStrategyBest(object):
    def choose_strategy(self, stock_id, name='baseline_strategy'):
        print('choose strategy:{}'.format(name))
        if name == 'golden_cross':
            return GoldenCrossSingleStrategy().compose_user_func(stock_id)
        return None

    def choose_stock_iterate(self):
        stock_ids = ['000001.XSHE', '600816.XSHG', '000063.XSHE']
        for stock_id in stock_ids:
            print('choose stock:{}'.format(stock_id))
            yield stock_id

    def compute_strategy(self, stock_id):
        # 您可以指定您要传递的参数
        user_func = self.choose_strategy(stock_id, name='golden_cross')
        print('use strategy:{}'.format(stock_id))
        run_func(**user_func)
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
    SingleStockStrategyBest().excute()
