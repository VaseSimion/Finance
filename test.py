import yfinance as yf
from datetime import date
from datetime import timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt

stock = "EVBG"
zile_in_trecut = 3   # cate zile o trecut de vineri pana acum:  daca e luni ii 3

if (date.today() + timedelta(-zile_in_trecut)).weekday() == 4:
    print("This is vineri")
figura = plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
for stock in ["^GSPC","SRNE","APHA","AU","SPCE","GSX","MRNA","IVR","EEX","WKHS","HBIO","PLCE","AHT","EPR","SNDX","PK",
              "MYOK","MFA","TRGP","RWT","GNPX","OMP","ARI","TH"]:
    try:
        weekly = yf.download(tickers=stock, interval="1d", period="3mo")
        closing = list(weekly["Close"])
        closing.reverse()

        today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]
        old_day = weekly.loc[str(date.today() + timedelta(-18 - zile_in_trecut))]
        print(stock, str(today["Close"] / old_day["Open"]))

        if today["Close"] / old_day["Open"] < 1:
            fig = mpf.plot(yf.download(tickers=stock, interval="1wk",
                                       start=str(date.today() + timedelta(-zile_in_trecut - 210)),
                                       end=str(date.today() + timedelta(-zile_in_trecut))), type='candle',
                           returnfig=True)
            plt.gca()
            plt.savefig("Images lose/" + stock + " " + str(round(today["Close"] / old_day["Open"], 2)) + " " +
                        str(date.today() + timedelta(-zile_in_trecut)) + ".png")
            plt.close()
        else:
            fig = mpf.plot(yf.download(tickers=stock, interval="1wk",
                                       start=str(date.today() + timedelta(-zile_in_trecut - 210)),
                                       end=str(date.today() + timedelta(-zile_in_trecut))), type='candle',
                           returnfig=True)
            plt.gca()
            plt.savefig("Images win/" + stock + " " + str(round(today["Close"] / old_day["Open"], 2)) + " " +
                        str(date.today() + timedelta(-zile_in_trecut)) + ".png")
            plt.close()
    except:
        print("There has been an error so something must have been fucked up")
        pass
