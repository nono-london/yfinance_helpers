from typing import Union

import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import (YFinanceConnectWithTicker, Ticker, Tickers)

pd.set_option('display.max_columns', None)


class YahooEarningsAnnouncement(YFinanceConnectWithTicker):
    def __init__(self, yahoo_tickers: Union[str, list], yf_ticker_connector=None):
        super().__init__(yahoo_tickers=yahoo_tickers, yf_ticker_connector=yf_ticker_connector)

    def get_next_earnings(self):
        if isinstance(self.yf_ticker_connector, Ticker):
            result_df: pd.DataFrame = self.yf_ticker_connector.get_calendar()
            result_df['yahoo_ticker'] = self.yf_ticker_connector.ticker
        elif isinstance(self.yf_ticker_connector, Tickers):
            result_df: pd.DataFrame = pd.DataFrame()
            for ticker in self.yf_ticker_connector.tickers:
                temp_df: pd.DataFrame = self.yf_ticker_connector.tickers[ticker].get_calendar()
                temp_df['yahoo_ticker'] = ticker
                result_df = result_df.append(temp_df)
        else:
            return

        result_df.reset_index(drop=False, inplace=True)
        result_df.rename(columns={'index': 'earnings_data', 'Value': 'expectations',
                                  0: 'min_exp', 1: 'max_exp'}, inplace=True, errors='ignore')
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooEarningsAnnouncement(yahoo_tickers=['ABMD', 'ALL', 'ANET', 'EQR', 'EXR', 'HSIC', 'IPGP',
                                                        'LNT', 'LVS', 'MCO', 'PANW', 'PEP', 'SO', 'SPLK',
                                                        'STZ', 'TGT', 'URI'])
    print(my_yahoo.get_next_earnings())
