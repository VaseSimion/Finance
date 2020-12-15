import tensorflow as tf
import numpy as np
import ReportModule as Rm
from datetime import date
from datetime import timedelta
import DatabaseStocks as Ds
import yfinance as yf
import ExtractData as Ed
import math
import AnalysisModule as Ass
import winsound
import MailModule as Mm
import PdfReport as Pr
import time


class PredictedStock:  # Class to save all predictions
    def __init__(self, stock_name, close_price, last_volume, predicted_price_increase, predicted_category_increase,
                 predicted_category_probabilities, supervised_category_prediction, supervised_probabilities,
                 success_score):
        self.name = stock_name
        self.price = close_price
        self.volume = last_volume
        self.predicted_price_increase = predicted_price_increase
        self.predicted_category_increase = predicted_category_increase
        self.supervised_category_prediction = supervised_category_prediction
        self.predicted_category_probabilities = predicted_category_probabilities
        self.supervised_probabilities = supervised_probabilities
        self.success_score = success_score


update_reports = True  # if this is false the report files don't get updated

report_name = "Reports/ReportFile " + str(date.today()) + ".txt"
report_file = open(report_name, "w+")

# Loading models
category_model = tf.keras.models.load_model("SavedModels/BestCategoryModel.h5")
model = tf.keras.models.load_model("SavedModels/BestPredictionModel.h5")
supervision_model = tf.keras.models.load_model("SavedModels/BestCategoryAlreadyPredictedModel.h5")

# Initializing all necessary lists
date_azi = date.today()
increment = 0
category_winners = []
prediction_winners = []
both_methods_winners = []
winners_as_objects = []
blacklist = ["SECI"]

listOfStocksToAnalyze = ["^GSPC"] + Ds.get_investing_lists()
for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 50 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
        weekly = yf.download(tickers=stock, interval="1wk", period="2y", threads=False)
        # Remove duplicates in so that in the days with splits/ dividents we dont remove them with the drop function
        weekly.index = weekly.index.where(~weekly.index.duplicated(), weekly.index + timedelta(1))
        # Remove all the NaN values
        for index, row in weekly.iterrows():
            if math.isnan(row["Close"]) or math.isnan(row["Volume"]):
                weekly = weekly.drop([index])

        # this is because if I just get the data by 1 week I have also the last friday so i get rid of the last entry
        if weekly.index.tolist()[-1] > (date_azi + timedelta(-date.weekday(date_azi))):
            weekly = weekly.drop([weekly.index.tolist()[-1]])
        if weekly.index.tolist()[-1] != (date_azi + timedelta(-date.weekday(date_azi))):
            print("Last date is not the last monday for " + stock)
            continue

        [price, volume] = Ed.get_latest_1_year_price_weekly_from_today(weekly)
        list_to_be_analyzed = price + volume
        if (list(weekly["Close"])[-1] <= 1) or (list(weekly["Volume"])[-1] <= 500000) or stock in blacklist:
            # Ignoring all stocks with a price smaller than 1$ low volume or blacklisted (not tradable)
            continue
        if len(list_to_be_analyzed) == 102:
            # here we predict the price increase and it needs to be calculated as a ratio of the last price
            price_predicted_value = model.predict(np.array([[list_to_be_analyzed]])) / list_to_be_analyzed[0]
            # here we calculate the price category where the stock lies in (0 - 0.8 - 1.2 - 2 - inf)
            predicted_value = category_model.predict(np.array([[list_to_be_analyzed]]))
            # making the prediction chance to be prediction probabilities and sum as 1
            total_predictions_chances = sum(predicted_value[0])
            predicted_value[0] = [round(100 * x / total_predictions_chances, 2) for x in predicted_value[0]]

            if 3 > price_predicted_value[0][0] > 1.3 or Ass.Decode(predicted_value[0]) > 1:
                # here we calculate the price category for supervision (0 - 0.8 - 1.2 - 2 - inf)
                supervision_predicted_value = supervision_model.predict(np.array([[list_to_be_analyzed]]))
                total_supervised_predictions_chances = sum(supervision_predicted_value[0])
                supervision_predicted_value[0] = [round(100 * x / total_supervised_predictions_chances, 2)
                                                  for x in supervision_predicted_value[0]]
                # Calculating local score based on the predictions
                local_score = Ass.calculate_score(price_predicted_value[0][0], predicted_value[0],
                                                  supervision_predicted_value[0])
                winners_as_objects.append(PredictedStock(stock_name=stock,
                                                         close_price=list(weekly["Close"])[-1],
                                                         last_volume=list(weekly["Volume"])[-1],
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

# Spit predictions into categories
for stocks_predicted in winners_as_objects:
    if stocks_predicted.predicted_price_increase > 1.3 and stocks_predicted.predicted_category_increase > 1:
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
    report_file.write("Script 1 predicted this:\n")
    for stock_performance in category_winners:
        Rm.write_stock(stock_performance, report_file)

    report_file.write("\n---------------------------------------------------------------------\n")
    report_file.write("Script 2 predicted this:\n")
    for stock_performance in prediction_winners:
        Rm.write_stock(stock_performance, report_file)

report_file.write("\nFor validation purposes this is the price list to use:\n")
for stock in both_methods_winners + prediction_winners:
    report_file.write("\"" + stock.name + "\",")

report_file.write("\nFor validation purposes this is the category list to use:\n")
for stock in both_methods_winners + category_winners:
    report_file.write("\"" + stock.name + "\",")

report_file.close()

Pr.write_the_report(both_methods_winners+category_winners+prediction_winners, Rm.return_report_from_3_weeks_ago())
print("Wait for the report to be written")
time.sleep(30)

# Send the email
Mm.send_mail([element.name + "(" + str(element.success_score) + ")" for element in both_methods_winners],
             [element.name + "(" + str(element.success_score) + ")" for element in category_winners],
             [element.name + "(" + str(element.success_score) + ")" for element in prediction_winners],
             file="Report " + str(date_azi) + ".pdf")

winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
