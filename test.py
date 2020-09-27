import yfinance as yf
from datetime import date
from datetime import timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt




print(calculate_score(0.91, [1,81,17,3], [1,8,92,1]))

print(date.today().weekday())

stock = "EVBG"
zile_in_trecut = 2   # cate zile o trecut de vineri pana acum:  daca e luni ii 3
if (date.today() + timedelta(-zile_in_trecut)).weekday() == 4:
    print("This is vineri")


for stock in ["^GSPC","SRNE","APHA"]:
    try:
        weekly = yf.download(tickers=stock, interval="1d", period="3mo")
        closing = list(weekly["Close"])
        closing.reverse()

        today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]
        old_day = weekly.loc[str(date.today() + timedelta(-18 - zile_in_trecut))]
        print(stock, str(today["Close"] / old_day["Open"]))
    except:
        print("error")