import yfinance as yf


class YFinanceConnectWithTicker(object):
    def __init__(self, yahoo_ticker: str):
        self.ticker = yahoo_ticker.upper()
        self.yahoo_connector_ticker = yf.Ticker(self.ticker)

    def print_class_variables(self):
        class_vars: dict = vars(self)
        print("#" * 20, "Class variables", "#" * 20)

        for item in class_vars:
            print(f"{item}: {class_vars[item]}")
        print("#" * 58)


if __name__ == '__main__':
    pass
