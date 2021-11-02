import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooFinancials(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str, yf_ticker_connector=None):
        super().__init__(yahoo_ticker=yahoo_ticker, yf_ticker_connector=yf_ticker_connector)
        self.summary_income_statement: list = ['Total Revenue', 'Ebit', 'Net Income', 'Net Income From Continuing Ops']

        self.debt_coverage_lower_limit:int=3
        self.debt_coverage_alert:bool=False

    def _clean_income_statement(self, income_statements_df: pd.DataFrame) -> pd.DataFrame:
        if income_statements_df.loc["Ebit", :].equals(income_statements_df.loc["Operating Income", :]):
            income_statements_df.drop(axis=0, index=["Operating Income"], inplace=True)
        else:
            print("Non identical: Ebit and Operating Income")
        return income_statements_df

    def _calculate_ebitda(self, income_statements_df: pd.DataFrame) -> pd.DataFrame:
        ebit = income_statements_df.loc['Ebit', :]
        tax = income_statements_df.loc['Income Tax Expense', :]

    def _calculate_interest_coverage_ratio(self, income_statements_df: pd.DataFrame) -> pd.DataFrame:
        ebit = income_statements_df.loc['Ebit', :].abs()
        interest_expense = income_statements_df.loc['Interest Expense', :].abs()
        interest_coverage_ratio = ebit.divide(interest_expense).astype(float).round(1)
        interest_coverage_ratio.name = "interest_coverage_ratio"
        income_statements_df = income_statements_df.append(interest_coverage_ratio)
        if (income_statements_df.loc["interest_coverage_ratio",:]<self.debt_coverage_lower_limit).any():
            print("Warning, detected potential problem with debt, interest_coverage_ratio is or has been less than 3")
            self.debt_coverage_alert=True
        return income_statements_df

    def get_yearly_income_statements(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_financials()
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df

    def get_quarterly_income_statements(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.quarterly_financials
        result_df = self._clean_income_statement(income_statements_df=result_df)

        result_df.to_csv(path_or_buf='test.csv', sep=',')
        result_df = self._calculate_interest_coverage_ratio(income_statements_df=result_df)
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df

    def get_yearly_balance_sheet(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_financials()
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df

    def get_quarterly_balance_sheet(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.quarterly_balance_sheet
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df

    def get_yearly_cash_flow(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.get_cashflow()
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df

    def get_quarterly_cash_flow(self, summarize_account: bool = True):
        result_df: pd.DataFrame = self.yf_ticker_connector.quarterly_cashflow
        if summarize_account:
            result_df = result_df.loc[self.summary_income_statement, :].copy()
        return result_df


if __name__ == '__main__':
    my_yahoo = YahooFinancials(yahoo_ticker='MKS.l')
    # print(my_yahoo.get_yearly_income_statements(summarize_account=False))
    print(my_yahoo.get_quarterly_income_statements(summarize_account=False))
    # print(my_yahoo.get_quarterly_balance_sheet(summarize_account=False))
    # print(my_yahoo.get_yearly_cash_flow(summarize_account=False))
    # print(my_yahoo.get_quarterly_cash_flow(summarize_account=False))
