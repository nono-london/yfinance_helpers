from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain


def test_update_mdb_with_tf():
    print(update_ib_options_chain(tickers=['aapl']))


if __name__ == '__main__':
    test_update_mdb_with_tf()
