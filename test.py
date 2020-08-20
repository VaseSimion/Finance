import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "EVBG"

for stock in ["VERI","NIO","SPCE","MRNA","NH"]:
    try:
        weekly = yf.download(tickers=stock, interval="1wk", period="1mo")
        closing = list(weekly["Close"])
        closing.reverse()
        if date.today().weekday() == 4:
            print("This is vineri")
            print(weekly)
            print(stock, str(closing[0]/closing[3]))
        else:
            print(weekly)
            print(stock, str(closing[0] / closing[3]))
    except:
        print("FFS")


