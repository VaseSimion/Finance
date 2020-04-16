import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "TSLA"
weekly = yf.download(tickers=stock, interval="1wk", period="1mo")
print(weekly["Close"])
