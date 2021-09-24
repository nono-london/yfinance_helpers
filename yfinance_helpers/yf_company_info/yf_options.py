import pandas as pd

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooOptionChain(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)

    def get_all_option_chains(self, order_by_volumes: bool = True, select_volume_over: int = 0):
        # https://aroussi.com/post/download-options-data
        print("#" * 20, f"Option Chain for ticker {self.ticker}", "#" * 20)
        expiries: tuple = self.yf_ticker_connector.options
        if len(expiries) == 0:
            print(f"Yahoo doesn't provide an option chain for ticker: {self.ticker}")
            print("#" * 50)
            return None
        result_df: pd.DataFrame = pd.DataFrame()
        for expiry in expiries:
            temp_df = self.get_options_chain_per_expiry(option_expiry=expiry)
            if temp_df is not None:
                result_df = result_df.append(temp_df, ignore_index=True)
        if order_by_volumes >= 0:
            result_df.sort_values(by=['volume', 'call_put'], ascending=[False, True],
                                  inplace=True, ignore_index=True)
        return self._reformat_option_chain_columns(result_df, select_volume_over=select_volume_over)

    def get_options_chain_per_expiry(self, option_expiry: str):
        try:
            option_chain = self.yf_ticker_connector.option_chain(date=option_expiry)
        except TypeError:
            print(f"Yahoo doesn't provide an option chain for ticker: {self.ticker}")
            print("#" * 50)
            return None
        call_df: pd.DataFrame = option_chain.calls
        call_df['call_put'] = 'Call'

        put_df: pd.DataFrame = option_chain.puts
        put_df['call_put'] = 'Put'
        result_df = call_df.append(put_df, ignore_index=True)
        result_df['expiry'] = option_expiry

        return result_df

    @staticmethod
    def _reformat_option_chain_columns(options_df: pd.DataFrame, select_volume_over: int = 0):

        options_df.rename(columns={'contractSymbol': 'contract_symbol', 'lastTradeDate': 'last_trade_date',
                                   'lastPrice': 'last_price', 'percentChange': 'percent_change',
                                   'openInterest': 'open_interest', 'impliedVolatility': 'implied_volatility',
                                   'inTheMoney': 'in_the_money', 'contractSize': 'contract_size',
                                   }, errors='ignore', inplace=True)

        options_df['volume'].fillna(value=0, inplace=True)
        options_df['volume'] = options_df['volume'].astype(int)
        if select_volume_over >= 0:
            options_df = options_df[options_df['volume'] > select_volume_over].copy()

        options_df['open_interest'].fillna(value=0, inplace=True)
        options_df = options_df.astype({"open_interest": int})

        options_df.drop(columns=['change', 'percent_change', 'in_the_money'],
                        inplace=True)
        return options_df


if __name__ == '__main__':
    my_yahoo = YahooOptionChain(yahoo_ticker='sgfy')

    print(my_yahoo.get_all_option_chains(select_volume_over=0, order_by_volumes=True))
