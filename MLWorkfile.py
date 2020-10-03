import tensorflow as tf
import numpy as np
import ReportModule as Rm
from datetime import date
from datetime import datetime, timedelta
import DatabaseStocks as Ds
import yfinance as yf
import ExtractData as Ed
import csv
import AnalysisModule as Ass
import winsound
import MailModule as Mm


class PredictedStock:
    def __init__(self, stock_name, close_price, predicted_price_increase, predicted_category_increase,
                 predicted_category_probabilities, supervised_category_prediction, supervised_probabilities,
                 success_score):
        self.name = stock_name
        self.price = close_price
        self.predicted_price_increase = predicted_price_increase
        self.predicted_category_increase = predicted_category_increase
        self.supervised_category_prediction = supervised_category_prediction
        self.predicted_category_probabilities = predicted_category_probabilities
        self.supervised_probabilities = supervised_probabilities
        self.success_score = success_score


update_reports = True

report_name = "Reports/ReportFile " + str(date.today()) + ".txt"
report_file = open(report_name, "w+")

category_model = tf.keras.models.load_model("SavedModels/BestCategoryModel.h5")
model = tf.keras.models.load_model("SavedModels/BestPredictionModel.h5")
supervision_model = tf.keras.models.load_model("SavedModels/BestCategoryAlreadyPredictedModel.h5")

date = date.today()
increment = 0
category_winners = []
prediction_winners = []
both_methods_winners = []
winners_as_objects = []

listOfStocksToAnalyze = ["^GSPC"] + Ds.get_investing_lists()
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
        weekly = weekly.drop([date.today() + timedelta(-1)])  # this is because if I just get the data by 1 week I have also the last friday
        # if date.today().weekday() == 6:
        #    weekly = weekly.drop([date.today() + timedelta(-2)])
        [price, volume] = Ed.get_latest_1_year_price_weekly_from_today(weekly)
        list_to_be_analyzed = price + volume
        if list(weekly["Close"])[-1] <= 1:
            continue
        if len(list_to_be_analyzed) == 102:
            price_predicted_value = model.predict(np.array([[list_to_be_analyzed]])) / list_to_be_analyzed[0]  # here we predict the price increase and it needs to be calculated as a ratio of the last price
            predicted_value = category_model.predict(np.array([[list_to_be_analyzed]]))  # here we calculate the price category where the stock lies in (0 - 0.8 - 1.2 - 2 - inf)
            total_predictions_chances = sum(predicted_value[0])
            predicted_value[0] = [round(100*x/total_predictions_chances, 2) for x in predicted_value[0]]  # making the prediction chance to be prediction probabilities and sum as 1

            if 2.5 > price_predicted_value[0][0] > 1.2 or Ass.Decode(predicted_value[0]) > 1:
                supervision_predicted_value = supervision_model.predict(np.array([[list_to_be_analyzed]]))  # here we calculate the price category for supervision in case we want to predict this and it's where the stock lies in (0 - 0.8 - 1.2 - 2 - inf)
                total_supervised_predictions_chances = sum(supervision_predicted_value[0])
                supervision_predicted_value[0] = [round(100 * x / total_supervised_predictions_chances, 2)
                                                  for x in supervision_predicted_value[0]]  # making the prediction chance to be prediction probabilities and sum as 1
                local_score = Ass.calculate_score(price_predicted_value[0][0], predicted_value[0],
                                                  supervision_predicted_value[0])
                winners_as_objects.append(PredictedStock(stock_name=stock,
                                                         close_price=list(weekly["Close"])[-1],
                                                         predicted_price_increase=price_predicted_value[0][0],
                                                         predicted_category_increase=Ass.Decode(predicted_value[0]),
                                                         supervised_category_prediction=
                                                         Ass.Decode(supervision_predicted_value[0]),
                                                         predicted_category_probabilities=predicted_value[0],
                                                         supervised_probabilities=supervision_predicted_value[0],
                                                         success_score=local_score))

                print("{} prediction has a score of {}".format(stock, local_score))
    except:
        print("Some shit happened with " + stock)

for stocks_predicted in winners_as_objects:
    if stocks_predicted.predicted_price_increase > 1.2 and stocks_predicted.predicted_category_increase > 1:
        both_methods_winners.append(stocks_predicted)
    elif stocks_predicted.predicted_category_increase < 1:
        prediction_winners.append(stocks_predicted)
    else:
        category_winners.append(stocks_predicted)

if update_reports:
    report_file.write("Both scripts predicted this:\n")
    for stock_performance in both_methods_winners:
        Rm.write_stock(stock_performance, report_file)

    report_file.write("\n---------------------------------------------------------------------\n")
    report_file.write("Category predicted this:\n")
    for stock_performance in category_winners:
        Rm.write_stock(stock_performance, report_file)

    report_file.write("\n---------------------------------------------------------------------\n")
    report_file.write("Price prediction scripts predicted this:\n")
    for stock_performance in prediction_winners:
        Rm.write_stock(stock_performance, report_file)

report_file.write("\nFor validation purposes this is the list to use:\n")
for stock in both_methods_winners+category_winners+prediction_winners:
    report_file.write("\"" + stock.name + "\",")

report_file.close()
Mm.send_mail([element.name + "(" + str(element.success_score) + ")" for element in both_methods_winners],
             [element.name + "(" + str(element.success_score) + ")" for element in category_winners],
             [element.name + "(" + str(element.success_score) + ")" for element in prediction_winners],
             file=report_name)

winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
