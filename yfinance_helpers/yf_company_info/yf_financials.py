import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooCompanyHolders(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector=None):
        super().__init__(yahoo_ticker=yahoo_ticker, yf_ticker_connector=yf_ticker_connector)
        self.default_financials: list = ['Total Revenue', 'Ebit', 'Net Income', 'Net Income From Continuing Ops']

    def get_yearly_financials(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_financials()
        if summarize_account:
            result_df = result_df.loc[self.default_financials, :].copy()
        return result_df

    def get_quarterly_financials(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.quarterly_financials
        if summarize_account:
            result_df = result_df.loc[self.default_financials, :].copy()
        return result_df

    def get_yearly_balance_sheet(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_financials()
        if summarize_account:
            result_df = result_df.loc[self.default_financials, :].copy()
        return result_df

    def get_quarterly_balance_sheet(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.quarterly_balance_sheet
        if summarize_account:
            result_df = result_df.loc[self.default_financials, :].copy()
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooCompanyHolders(yahoo_ticker='fgp.l')
    # print(my_yahoo.get_yearly_financials(summarize_account=False))
    # print(my_yahoo.get_quarterly_financials(summarize_account=True))
    print(my_yahoo.get_quarterly_balance_sheet(summarize_account=False))