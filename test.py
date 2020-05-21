import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "TSLA"

for stock in ["M","TEX","CLB","GPS","DO","NBR","VAL","HTZ","SIX","TSLA","TUP","RAD"]:
    try:
        weekly = yf.download(tickers=stock, interval="1wk", period="1mo")
        closing = list(weekly["Close"])
        closing.reverse()
        print(stock, str(closing[1]/closing[4]))
    except:
        print("FFS")
if date.today().weekday() == 0 or date.today().weekday() == 5 or date.today().weekday() == 6:
    print("gg")
