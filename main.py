from yfinance_helpers.app_config import pack_python_libs_in_path

pack_python_libs_in_path()

from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain
from multiprocessing import freeze_support


def main():
    pack_python_libs_in_path()
    update_ib_options_chain()


if __name__ == '__main__':
    freeze_support()
    main()
