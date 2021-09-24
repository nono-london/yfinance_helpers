import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooAnalystRecommendation(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector=None):
        super().__init__(yahoo_ticker, yf_ticker_connector=yf_ticker_connector, )

    def get_analyst_recommendations(self):
        print("#" * 20, f"Analyst Recommendations {self.ticker}", "#" * 20)
        result_df: pd.DataFrame = self.yf_ticker_connector.get_recommendations()
        if result_df is None or len(result_df) == 0:
            print(f"Yahoo doesn't provide any analyst recommendation for {self.ticker}")
            return None
        result_df.reset_index(drop=False, inplace=True)
        result_df.rename(columns={'Date': 'date', 'Firm': 'analyst', "To Grade": "to_grade",
                                  'From Grade': 'from_grade', 'Action': 'action'}, inplace=True)
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooAnalystRecommendation(yahoo_ticker='sgfy')
    print(my_yahoo.get_analyst_recommendations())
