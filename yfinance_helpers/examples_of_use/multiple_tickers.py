import yfinance as yf
tickers = yf.Tickers('msft aapl goog')
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
print(tickers.tickers['MSFT'].info)
print(tickers.tickers['MSFT'].earnings_dates)
print(tickers.tickers['AAPL'].history(period="1mo"))
print(tickers.tickers['GOOG'].actions)