from yfinance_helpers.yf_company_info.yf_analysts import YahooAnalystRecommendation as _YahooAnalystRecommendation
from yfinance_helpers.yf_company_info.yf_dividends import YahooDividends as _YahooDividends
from yfinance_helpers.yf_company_info.yf_earnings import YahooEarningsAnnouncement as _YahooEarningsAnnouncement
from yfinance_helpers.yf_company_info.yf_fundamentals import YahooFundamentals as _YahooFundamentals
from yfinance_helpers.yf_company_info.yf_holders import YahooCompanyHolders as _YahooCompanyHolders
from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker as _YFinanceConnectWithTicker


class YahooGetWithTicker(_YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)
        self.yf_analyst = _YahooAnalystRecommendation(yahoo_ticker=self.ticker,
                                                      yf_ticker_connector=self.yf_ticker_connector)
        self.yf_earnings = _YahooEarningsAnnouncement(yahoo_ticker=self.ticker,
                                                      yf_ticker_connector=self.yf_ticker_connector)
        self.yf_dividends = _YahooDividends(yahoo_ticker=self.ticker,
                                            yf_ticker_connector=self.yf_ticker_connector)
        self.yf_fundamentals = _YahooFundamentals(yahoo_ticker=self.ticker,
                                                  yf_ticker_connector=self.yf_ticker_connector)

        self.yf_holders = _YahooCompanyHolders(yahoo_ticker=self.ticker,
                                               yf_ticker_connector=self.yf_ticker_connector)


if __name__ == '__main__':
    my_yf_getter = YahooGetWithTicker(yahoo_ticker='pfe')
    print(my_yf_getter.yf_analyst.get_analyst_recommendations())
    print(my_yf_getter.yf_earnings.get_next_earnings())
    print(my_yf_getter.yf_dividends.get_dividend_history())
    print(my_yf_getter.yf_fundamentals.get_fundamentals())
    print(my_yf_getter.yf_holders.get_holders())
