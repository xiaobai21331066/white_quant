import abc
class SingleStrategyBase(metaclass=abc.ABCMeta):
    @classmethod
    def compose_user_func(cls, stock_id):
        user_func = {'init': cls.init(stock_id),
                     'before_trading': cls.before_trading,
                     'handle_bar': cls.handle_bar,
                     'config': cls.config()}
        return user_func

    @staticmethod
    @abc.abstractmethod
    def config():
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def init(stock_id):
        raise NotImplementedError

    @staticmethod
    def before_trading(context):
        return None

    @staticmethod
    @abc.abstractmethod
    def handle_bar(context, bar_dict):
        raise NotImplementedError

    @staticmethod
    def after_trading(cls):
        return None
