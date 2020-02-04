# this extracts data from an API for finance, but this API was lagging so I switched to yfinance
from urllib.request import urlopen
import json
import pandas as pd


class DayResults:
    def __init__(self, dateday, openprice, closeprice, lowprice, highprice, tradevolume):
        self.date = dateday
        self.open = openprice
        self.close = closeprice
        self.low = lowprice
        self.high = highprice
        self.volume = tradevolume

    def print_day(self):
        print("On {} the price opened at {} and closed at {}".format(self.date, self.open, self.close))


class MarketIndex:
    def __init__(self, stockname):
        self.history = []
        self.day = DayResults(0, 0, 0, 0, 0, 0)
        self.name = stockname

    def reset(self):
        self.history = []

    def update(self, start_data, end_data):
        self.reset()
        url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" + self.name + "?from=" + start_data
               + "&to=" + end_data)
        response = urlopen(url)
        results = json.loads(response.read().decode("utf-8"))
        for day in results['historical']:
            self.history.append(DayResults(day['date'], day['open'], day['close'], day['low'],
                                           day['high'], day['volume']))

    def get_data_as_dataframe(self):
        datelist, opendata, closedata, lowdata, highdata, volumedata = [], [], [], [], [], []
        for day in self.history:
            datelist.append(day.date)
            opendata.append(day.open)
            closedata.append(day.close)
            highdata.append(day.high)
            lowdata.append(day.low)
            volumedata.append(day.volume)
        dataframe = pd.DataFrame(list(zip(opendata, highdata, lowdata, closedata, volumedata)),
                                 columns=["Open", "High", "Low", "Close", "Volume"], index=pd.to_datetime(datelist))
        #        print(df)
        return dataframe

    def print_last_days(self):
        for self.day in self.history:
            self.day.print_day()
        print()

#   Apple = MarketIndex("AAPL")
#   Apple.update("2020-01-10", "2020-01-23")
#   Apple.print_last_days()

#   print()
