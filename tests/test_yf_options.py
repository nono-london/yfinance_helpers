from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain


def update_mdb_with_tf():
    update_ib_options_chain()


if __name__ == '__main__':
    update_mdb_with_tf()