import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "TSLA"
weekly = yf.download(tickers=stock, interval="1wk", period="2y")
print(weekly["Close"])
if date.today().weekday() == 0 or date.today().weekday() == 5 or date.today().weekday() == 6:
    print("gg")
