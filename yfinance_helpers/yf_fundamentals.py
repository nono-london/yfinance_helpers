from datetime import datetime

import pandas as pd

from yfinance_helpers.yf_connectors import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooFundamentals(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)

        self.number_of_employee: int = None
        self.shares_outstanding: int = None
        self.website: str = None
        self.isin_code: str = None

        self.current_dividend_per_year: float = None
        self.last_dividend_ex_date: datetime.date = None

        self.trailing_pe: float = None
        self.forward_pe: float = None

        self.short_date: datetime.date = None
        self.short_percent_of_float: float = None
        self.shares_short: int = None
        self.short_days_to_cover: float = None

        self.average_10_days_volume: int = None

    def get_fundamentals(self):
        ticker_info: dict = self.yahoo_connector_ticker.get_info()

        self.number_of_employee = self._get_fundamental_from_ticker_info(ticker_info, 'fullTimeEmployees')
        self.website = self._get_fundamental_from_ticker_info(ticker_info, 'website')
        self.shares_outstanding = self._get_fundamental_from_ticker_info(ticker_info, 'sharesOutstanding')

        self.average_10_days_volume = self._get_fundamental_from_ticker_info(ticker_info, 'averageDailyVolume10Day')

        self.trailing_pe = self._get_fundamental_from_ticker_info(ticker_info, 'trailingPE')
        self.forward_pe = self._get_fundamental_from_ticker_info(ticker_info, 'forwardPE')

        self.short_date = self._convert_unix_date_to_datetime(
            self._get_fundamental_from_ticker_info(ticker_info, 'dateShortInterest')
        )
        self.shares_short = self._get_fundamental_from_ticker_info(ticker_info, 'sharesShort')
        self.short_percent_of_float = self._get_fundamental_from_ticker_info(ticker_info, 'shortPercentOfFloat')
        try:
            self.short_days_to_cover = round(self.shares_short / self.average_10_days_volume, 2)
        except TypeError:
            pass
        self.current_dividend_per_year = self._get_fundamental_from_ticker_info(ticker_info, 'dividendRate')
        self.last_dividend_ex_date = self._convert_unix_date_to_datetime(
            self._get_fundamental_from_ticker_info(ticker_info, 'exDividendDate')
        )
        self.isin_code = self.yahoo_connector_ticker.isin
        self.print_class_variables()
        return vars(self)

    def _get_fundamental_from_ticker_info(self, ticker_info: dict, fundamental: str):
        try:
            return ticker_info[fundamental]
        except KeyError:
            print(f'Fundamental "{fundamental}" is not available for ticker "{self.ticker}".')
            return None

    @staticmethod
    def _convert_unix_date_to_datetime(date_to_convert):
        try:
            return datetime.fromtimestamp(date_to_convert).date()
        except TypeError:
            return None


if __name__ == '__main__':
    my_yahoo = YahooFundamentals(yahoo_ticker='sgfy')
    print(my_yahoo.get_fundamentals())
