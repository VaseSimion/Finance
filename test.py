import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "TSLA"
#weekly = yf.download(tickers=stock, interval="1wk", start="2019-01-11", end="2020-04-04")
#print(weekly["Close"])

for stock in ["NBR","SM","RAD","GNC","FTI","QEP","SLB","UAA","LPI","SGMS","CAL","ADI"]:
    weekly = yf.download(tickers=stock, interval="1wk", period="1mo")
    closing = list(weekly["Close"])
    closing.reverse()
    print(stock, str(closing[1]/closing[4]))

if date.today().weekday() == 0 or date.today().weekday() == 5 or date.today().weekday() == 6:
    print("gg")
