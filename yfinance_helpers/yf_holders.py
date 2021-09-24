import pandas as pd
from yfinance_helpers.yf_connectors import YFinanceConnectWithTicker
import pandas as pd

from yfinance_helpers.yf_connectors import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooCompanyHolders(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)

    def get_holders(self, aggregate_mutual_funds: bool = True):
        result_df: pd.DataFrame = self.yahoo_connector_ticker.get_institutional_holders()
        result_df['holder_type'] = 'institutional'
        if aggregate_mutual_funds:
            temp_df = self.yahoo_connector_ticker.get_mutualfund_holders()
            temp_df['holder_type'] = 'mutual_fund'
            result_df = result_df.append(temp_df, ignore_index=True)

        result_df.rename(columns={'Holder': 'holders', 'Shares': 'shares',
                                  'Date Reported': 'reported_date',
                                  '% Out': 'percent_out', 'Value': 'notional'},
                         inplace=True, errors='ignore')
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooCompanyHolders(yahoo_ticker='sgfy')
    print(my_yahoo.get_holders())
