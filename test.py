import yfinance as yf
from datetime import date
from datetime import timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt
import math
list_of_stocks = []
print(date.today().weekday())

stock = "CTL"
zile_in_trecut = 4   # cate zile o trecut de vineri pana acum:  daca e luni ii 3
if (date.today() + timedelta(-zile_in_trecut)).weekday() == 4:
    print("This is vineri")

weekly = yf.download(tickers=stock, interval="1wk", period="2y")
weekly = weekly.drop(
    [date.today() + timedelta(-1)])  # this is because if I just get the data by 1 week I have also the last friday
weekly = weekly.drop([date.today() + timedelta(-8)])
weekly = weekly.drop([date.today() + timedelta(-15)])
weekly = weekly.drop([date.today() + timedelta(-22)])


print(weekly)

for stock in ["^GSPC"]:
    try:
        weekly = yf.download(tickers=stock, interval="1d", period="6mo")
        closing = list(weekly["Close"])
        closing.reverse()
        today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]
        print(str(date.today() + timedelta(- zile_in_trecut)))
        old_day = weekly.loc[str(date.today() + timedelta(-18 - zile_in_trecut))]
        print(str(date.today() + timedelta(-18 - zile_in_trecut)))
        print(stock, str(today["Close"] / old_day["Open"]))
        list_of_stocks.append([stock, old_day["Open"], str(today["Close"] / old_day["Open"])])
    except:
        print("error")

for element in list_of_stocks:
    print(element[0] + " bought at " + str(element[1]) + " had an increase of " + str(element[2]))