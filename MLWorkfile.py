import tensorflow as tf
import numpy as np
import ReportModule as Rm
from datetime import date
from datetime import datetime
import DatabaseStocks as Ds
import yfinance as yf
import ExtractData as Ed
import csv
import AnalysisModule as Ass
import winsound

update_reports = True
prediction_file = open('predictions.csv', 'w')
prediction_writer = csv.writer(prediction_file, delimiter=',', lineterminator='\n',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)

category_prediction_file = open('predictions_category.csv', 'w')
category_prediction_writer = csv.writer(category_prediction_file, delimiter=',', lineterminator='\n',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

name = "Reports/ReportFile " + str(date.today()) + ".txt"
report_file = open(name, "w+")

category_model = tf.keras.models.load_model("SavedModels/BestCategoryModel.h5")
model = tf.keras.models.load_model("SavedModels/BestPredictionModel.h5")

date = date.today()
prediction_writer.writerow([str(date)])
category_prediction_writer.writerow([str(date)])
date = datetime.combine(date.today(), datetime.min.time())
increment = 0
category_winners = []
prediction_winners = []
both_methods_winners = []

listOfStocksToAnalyze = Ds.get_investing_lists()
for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 50 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
    #        weekly = yf.download(tickers=stock, interval="1wk", start="2019-01-11", end="2020-04-04")
        weekly = yf.download(tickers=stock, interval="1wk", period="2y")
        [price, volume] = Ed.get_latest_1_year_price_weekly_from_today(weekly)
        list_to_be_analyzed = price + volume
        if len(list_to_be_analyzed) == 102:
            price_predicted_value = model.predict(np.array([[list_to_be_analyzed]])) / list_to_be_analyzed[0]
            prediction_writer.writerow([stock, price_predicted_value[0][0]])
            prediction_file.flush()
            if 2 > price_predicted_value[0][0] > 1.15:
                prediction_winners.append([stock, price_predicted_value[0][0], list(weekly["Close"])[-1]])
            print("{} prediction is {}".format(stock, price_predicted_value[0][0]))

            predicted_value = category_model.predict(np.array([[list_to_be_analyzed]]))
            total_predictions_chances = sum(predicted_value[0])
            predicted_value[0] = [round(100*x/total_predictions_chances, 2) for x in predicted_value[0]]
            category_prediction_writer.writerow([stock] + [Ass.Decode(predicted_value[0])] + list(predicted_value[0]))
            category_prediction_file.flush()
            if Ass.Decode(predicted_value[0]) > 1:
                if len(prediction_winners) > 0 and stock == prediction_winners[-1][0]:
                    both_methods_winners.append(prediction_winners[-1] + [Ass.Decode(predicted_value[0])] +
                                                list(predicted_value[0]))
                    prediction_winners.pop()
                else:
                    category_winners.append([stock] + [price_predicted_value[0][0]] + [list(weekly["Close"])[-1]] +
                                            [Ass.Decode(predicted_value[0])] + list(predicted_value[0]))
            print("{} prediction is {} with {}".format(stock, Ass.Decode(predicted_value[0]), predicted_value[0]))
    except:
        print("Some shit happened")

if update_reports:
    report_file.write("Both scripts predicted this:\n")
    for stock_performance in both_methods_winners:
        Rm.append_both(stock_performance, report_file)

    report_file.write("\n---------------------------------------------------------------------\n")
    report_file.write("Category predicted this:\n")
    for stock_performance in category_winners:
        Rm.append_category(stock_performance, report_file)

    report_file.write("\n---------------------------------------------------------------------\n")
    report_file.write("Price prediction scripts predicted this:\n")
    for stock_performance in prediction_winners:
        Rm.append_price_prediction(stock_performance, report_file)

report_file.write("\nFor validation purposes this is the list to use:\n")
for stock in both_methods_winners+category_winners+prediction_winners:
    report_file.write("\"" + stock[0] + "\",")

prediction_file.close()
category_prediction_file.close()
report_file.close()
winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
