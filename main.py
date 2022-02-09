from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain
from multiprocessing import freeze_support


def main():
    update_ib_options_chain()


if __name__ == '__main__':
    freeze_support()
    main()
