import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "EVBG"

for stock in ["^GSPC", "BLDP","NIO","BGG","DLPH","MRNA","TLRD"]:
    try:
        weekly = yf.download(tickers=stock, interval="1d", period="1mo")
        closing = list(weekly["Close"])
        closing.reverse()
        if date.today().weekday() == 4:
            #print("This is vineri")
            #print(weekly)
            today = weekly.loc[str(date.today())]
            old_day = weekly.loc[str(date.today()+timedelta(-18))]
            #print(today["Close"])
            #print(old_day["Open"])
            print(stock, str(today["Close"]/old_day["Open"]))
        else:
            print(weekly)
            print(stock, str(closing[0] / closing[3]))
    except:
        #print("FFS")
        pass

