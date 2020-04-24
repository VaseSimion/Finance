import tensorflow as tf
import numpy as np
import os
from datetime import date
from datetime import datetime
import DatabaseStocks as Ds
import yfinance as yf
import ExtractData as Ed
import csv
import AnalysisModule as Ass


prediction_file = open('predictions.csv', 'w')
prediction_writer = csv.writer(prediction_file, delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)

model = tf.keras.models.load_model("SavedModels/CategoryModel.h5")

print(model.summary())

date = date.today()
prediction_writer.writerow([str(date)])
date = datetime.combine(date.today(), datetime.min.time())
increment = 0

listOfStocksToAnalyze = Ds.get_lists()

for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 50 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
        weekly = yf.download(tickers=stock, interval="1wk", start="2019-01-11", end="2020-04-04")
    #        weekly = yf.download(tickers=stock, interval="1wk", period="2y")
        financial = Ed.get_financial_data(stock)
        financial_values = Ed.get_latest_3_year_quarterly(financial, date)
        [price, volume] = Ed.get_latest_1_year_price_weekly_from_today(weekly)
        list_to_be_analyzed = price + volume + financial_values
        if len(list_to_be_analyzed) == 150:
            predicted_value = model.predict(np.array([[list_to_be_analyzed]])) / list_to_be_analyzed[0]
            prediction_writer.writerow([stock] + [Ass.Decode(predicted_value[0])] + list(predicted_value[0]))
            prediction_file.flush()
            print("{} prediction is {} with {}".format(stock, Ass.Decode(predicted_value[0]), predicted_value[0]))
    except:
        print("Shit happened")
prediction_file.close()
