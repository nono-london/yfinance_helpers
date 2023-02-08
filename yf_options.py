from yfinance_helpers.app_config import pack_python_libs_in_path
pack_python_libs_in_path()

from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain


def get_option_chain_from_yahoo():
    pack_python_libs_in_path()
    update_ib_options_chain()


if __name__ == '__main__':
    get_option_chain_from_yahoo()
