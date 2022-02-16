from typing import Union, Optional

import yfinance as yf
from yfinance import Ticker, Tickers


class YFinanceConnectWithTicker:
    def __init__(self, yahoo_tickers: Union[str, list], yf_ticker_connector: Optional[Ticker] = None):
        if isinstance(yahoo_tickers, str):
            self.tickers: Union[str, list] = yahoo_tickers.upper()
        elif isinstance(yahoo_tickers, list):
            self.tickers: Union[str, list] = [yahoo_ticker.upper() for yahoo_ticker in yahoo_tickers]

        if yf_ticker_connector is None and isinstance(self.tickers, str):
            self.yf_ticker_connector = yf.Ticker(self.tickers)
        elif yf_ticker_connector is None and isinstance(self.tickers, list):
            self.yf_ticker_connector = yf.Tickers(self.tickers)
        else:
            self.yf_ticker_connector = yf_ticker_connector

    def print_class_variables(self):
        class_vars: dict = vars(self)
        print("#" * 20, "Class variables", "#" * 20)

        for item in class_vars:
            print(f"{item}: {class_vars[item]}")
        print("#" * 58)


if __name__ == '__main__':
    my_yf_connector = YFinanceConnectWithTicker(yahoo_tickers=['sgfy', 'aapl'])
    my_yf_connector.print_class_variables()
