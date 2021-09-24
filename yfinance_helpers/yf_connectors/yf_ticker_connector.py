import yfinance as yf
from yfinance import Ticker


class YFinanceConnectWithTicker(object):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector: Ticker = None):
        self.ticker = yahoo_ticker.upper()
        if yf_ticker_connector is None:
            self.yf_ticker_connector = yf.Ticker(self.ticker)
        else:
            self.yf_ticker_connector = yf_ticker_connector

    def print_class_variables(self):
        class_vars: dict = vars(self)
        print("#" * 20, "Class variables", "#" * 20)

        for item in class_vars:
            print(f"{item}: {class_vars[item]}")
        print("#" * 58)


if __name__ == '__main__':
    my_yf_connector = YFinanceConnectWithTicker(yahoo_ticker='sgfy')
    my_yf_connector.print_class_variables()
