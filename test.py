import yfinance as yf
from datetime import date
from datetime import timedelta
import ReportModule as Rm
import mplfinance as mpf
import matplotlib.pyplot as plt
import math
list_of_stocks = []
print(date.today().weekday())

stock = "AAPL"
zile_in_trecut = 1   # cate zile o trecut de vineri pana acum:  daca e luni ii 3
if (date.today() + timedelta(-zile_in_trecut)).weekday() == 4:
    print("This is vineri")

weekly = yf.download(tickers=stock, interval="1wk", period="2y")
weekly = weekly.drop([date.today() + timedelta(-1)])  # this is because if I just get the data by 1 week I have also the last friday

print(weekly)

print(Rm.return_report_from_3_weeks_ago())
