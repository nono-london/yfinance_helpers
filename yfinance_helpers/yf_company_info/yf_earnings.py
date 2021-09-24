import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooEarningsAnnouncement(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector=None):
        super().__init__(yahoo_ticker=yahoo_ticker, yf_ticker_connector=yf_ticker_connector)

    def get_next_earnings(self):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_calendar()
        result_df.reset_index(drop=False, inplace=True)
        result_df.rename(columns={'index': 'earnings_data', 'Value': 'expectations',
                                  0: 'min_exp', 1: 'max_exp'}, inplace=True, errors='ignore')
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooEarningsAnnouncement(yahoo_ticker='sgfy')
    print(my_yahoo.get_next_earnings())
