import logging
from pathlib import Path

from dotenv import load_dotenv

from yfinance_helpers.app_config import logging_config
from yfinance_helpers.yf_company_info.yf_options import update_ib_options_chain

logger = logging.getLogger(Path(__file__).name)


def main():
    logger.info(f"{'#' * 10} Starting options chain")
    update_ib_options_chain()


if __name__ == '__main__':
    logging_config(log_level=logging.INFO,
                   force_local_folder=False)
    load_dotenv()
    main()
