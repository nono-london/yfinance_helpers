import asyncio
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from postgresql_helpers.mdb_classes.async_postgres_class import AsyncPostGresConnector

from yfinance_helpers.yf_connectors.yf_ticker_connector import YFinanceConnectWithTicker

pd.set_option('display.max_columns', None)


class YahooOptionChain(YFinanceConnectWithTicker):
    def __init__(self, yahoo_ticker: str):
        super().__init__(yahoo_ticker)
        self.DATABASE_NAME: str = 'helios_finance'
        self.mdb_upper = AsyncPostGresConnector(mdb_name=self.DATABASE_NAME)
        self.ticker = yahoo_ticker.upper()
        self.upload_date: datetime.date = datetime.utcnow().date() - timedelta(days=1)

    def get_all_option_chains(self, order_by_volumes: bool = True, select_volume_over: int = 0):
        # https://aroussi.com/post/download-options-data
        print("#" * 20, f"Option Chain for ticker {self.ticker}", "#" * 20)
        try:
            expiries: tuple = self.yf_ticker_connector.options
        except Exception as ex:
            print(f'Error while getting options for ticker: "{self.ticker}\n'
                  f'Error is: {ex}"')
            # Seems like there is a bug when no option are available
            return None

        if len(expiries) == 0:
            print(f"Yahoo doesn't provide an option chain for ticker: {self.ticker}")
            print("#" * 50)
            return None
        result_df: pd.DataFrame = pd.DataFrame()
        for expiry in expiries:
            temp_df = self.get_options_chain_per_expiry(option_expiry=expiry)
            if temp_df is not None and not temp_df.empty:
                result_df = pd.concat([result_df, temp_df], ignore_index=True)
        if order_by_volumes >= 0:
            result_df.sort_values(by=['volume', 'call_put'], ascending=[False, True],
                                  inplace=True, ignore_index=True)

        result_df = self._reformat_option_chain_columns(result_df, select_volume_over=select_volume_over)
        self.upload_to_mdb(ticker=self.ticker, options_df=result_df, upload_date=self.upload_date)
        asyncio.get_event_loop().run_until_complete(self.mdb_upper.close_connection())

        return result_df

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
        result_df = pd.concat([call_df, put_df], ignore_index=True, )
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

    def upload_to_mdb(self, ticker: str, options_df: pd.DataFrame, upload_date: datetime.date):
        print(options_df)

        sql_string: str = """
        INSERT INTO t_histo_options(
                ticker_id, 
                upload_date, last_trade_datetime, 
                strike, bid, ask, last_price, volume, 
                open_interest, implied_volatility,
                    currency, call_put, expiry
                    )
              
                
          SELECT  ticker_id, 
            $1,$2, 
            $3, $4, $5, $6, $7, 
            $8, $9, 
            $10, $11, $12
                 
          FROM d_ticker
          WHERE yahoo_ticker=$13

        ON CONFLICT ON CONSTRAINT "t_histo_options_ticker_id_upload_date_strike_expiry_call_pu_key"
        DO UPDATE 
        SET last_trade_datetime=EXCLUDED.last_trade_datetime, 
            last_price=EXCLUDED.last_price,
            volume=EXCLUDED.volume,
            open_interest=EXCLUDED.open_interest,
            implied_volatility=EXCLUDED.implied_volatility
        """
        for index, row in options_df.iterrows():
            sql_variables: tuple = (upload_date, row['last_trade_date'],
                                    row['strike'], row['bid'], row['ask'], row['last_price'], row['volume'],
                                    row['open_interest'], row['implied_volatility'],
                                    row['currency'], row['call_put'], datetime.strptime(row['expiry'], "%Y-%m-%d"),
                                    ticker,
                                    )
            asyncio.get_event_loop().run_until_complete(self.mdb_upper.execute_one_query(sql_query=sql_string,
                                                                                         sql_variables=sql_variables,
                                                                                         close_connection=False
                                                                                         ))


def update_ib_options_chain(tickers: Optional[list] = None):
    mdb_getter = AsyncPostGresConnector(mdb_name='helios_finance')
    sql_string: str = """
                    SELECT UPPER(a.yahoo_ticker) "yahoo_ticker"
                FROM d_ticker a INNER JOIN d_security b USING(security_id)
                WHERE a.is_active=True AND b.is_active=True
                        AND b.security_type NOT IN ('Currency', 'Warrant')
                        AND a.yahoo_ticker NOT LIKE ('%.%')
                ORDER BY a.yahoo_ticker 
    
    """
    if not tickers:
        ticker_df: pd.DataFrame = asyncio.get_event_loop().run_until_complete(
            mdb_getter.fetch_all_as_pd(sql_query=sql_string))
        tickers: list = ticker_df['yahoo_ticker'].to_list()
    results: list = list()
    fails: list = list()
    for ticker in tickers:
        my_yahoo = YahooOptionChain(yahoo_ticker=ticker)
        temp_df: pd.DataFrame = my_yahoo.get_all_option_chains(select_volume_over=0, order_by_volumes=True)
        if temp_df is not None and len(temp_df) > 0:
            results.append(dict(ticker=ticker, success=True))
        else:
            results.append(dict(ticker=ticker, success=False))
            fails.append(dict(error=ticker))
    fail_df = pd.DataFrame(fails)
    fail_df.to_csv("error_with_options.csv", sep=',', index=False)
    return results


if __name__ == '__main__':
    update_ib_options_chain(tickers=None)
    exit(0)
    my_yahoo = YahooOptionChain(yahoo_ticker='spy')

    print(my_yahoo.get_all_option_chains(select_volume_over=0, order_by_volumes=True))
