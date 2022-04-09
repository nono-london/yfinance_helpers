from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain


def get_option_chain_from_yahoo():
    update_ib_options_chain()

if __name__ == '__main__':
    get_option_chain_from_yahoo()