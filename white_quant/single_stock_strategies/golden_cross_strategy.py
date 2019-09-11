from .base_strategy import SingleStrategyBase
from rqalpha.api import *
import talib
import time

class GoldenCrossSingleStrategy(SingleStrategyBase):

    def config():
        print('get config from golden cross.')
        config = {}
        return config

    def init(stock_id):
        """decorater"""
        print('call decorater: time{}', time.time())
        def add_stock(context):
            """add stock"""
            print('call add_stock: time{}', time.time())
            logger.info("init")
            context.s1 = stock_id
            context.SHORTPERIOD = 20
            context.LONGPERIOD = 120
            update_universe(context.s1)
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

    def handle_bar(context, bar_dict):
        prices = history_bars(context.s1, context.LONGPERIOD + 1, '1d', 'close')

        # 使用talib计算长短两根均线，均线以array的格式表达
        short_avg = talib.SMA(prices, context.SHORTPERIOD)
        long_avg = talib.SMA(prices, context.LONGPERIOD)
        logger.info('short:{}, long:{}'.format(short_avg[-1], long_avg[-1]))
        # plot("short avg", short_avg[-1])
        # plot("long avg", long_avg[-1])

        # 计算现在portfolio中股票的仓位
        cur_position = context.portfolio.positions[context.s1].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close
        # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
        if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and cur_position > 0:
            # 进行清仓
            logger.info('进行清仓')
            order_target_value(context.s1, 0)

        # 如果短均线从下往上突破长均线，为入场信号
        if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
            # 满仓入股
            logger.info('满仓入股')
            order_target_value(context.s1, context.portfolio.cash)
