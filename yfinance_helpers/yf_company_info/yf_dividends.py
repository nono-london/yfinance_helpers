import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooDividends(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector=None):
        super().__init__(yahoo_ticker=yahoo_ticker, yf_ticker_connector=yf_ticker_connector)

    def get_dividend_history(self):
        result_df: pd.DataFrame = self.yf_ticker_connector.dividends.to_frame()
        result_df.reset_index(drop=False, inplace=True)
        result_df.rename(columns={'Date': 'ex_date', 'Dividends': 'gross_dividend'}, errors='ignore', inplace=True)

        return result_df


if __name__ == '__main__':
    my_yahoo = YahooDividends(yahoo_ticker='pfe')
    print(my_yahoo.get_dividend_history())
