import pandas as pd

from yfinance_helpers.yf_connectors import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooEarningsAnnouncement(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)


    def get_next_earnings(self):
        result_df: pd.DataFrame = self.yahoo_connector_ticker.get_calendar()
        result_df.reset_index(drop=False, inplace=True)
        result_df.rename(columns={'index': 'earnings_data', 'Value': 'expectations',
                                  0: 'min_exp', 1: 'max_exp'}, inplace=True, errors='ignore')
        return result_df




if __name__ == '__main__':
    my_yahoo = YahooEarningsAnnouncement(yahoo_ticker='sgfy')
    print(my_yahoo.get_next_earnings())
