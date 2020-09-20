import yfinance as yf
from datetime import date
from datetime import timedelta

stock = "EVBG"

for stock in ["^GSPC","SRNE","APHA","AU","SPCE","GSX","MRNA","IVR","EEX","WKHS","HBIO","PLCE","AHT","EPR","SNDX",
              "PK","MYOK","MFA","TRGP","RWT","GNPX","OMP","ARI","TH"]:
    try:
        weekly = yf.download(tickers=stock, interval="1d", period="1mo")
        closing = list(weekly["Close"])
        closing.reverse()
        if (date.today()+timedelta(-2)).weekday() == 4:
            print("This is vineri")
            #print(weekly)
            today = weekly.loc[str(date.today()+timedelta(-2))]
            old_day = weekly.loc[str(date.today()+timedelta(-20))]
            #print(today["Close"])
            #print(old_day["Open"])
            print(stock, str(today["Close"]/old_day["Open"]))
        else:
            print(weekly)
            print(stock, str(closing[0] / closing[3]))
    except:
        #print("FFS")
        pass

