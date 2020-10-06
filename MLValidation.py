import tensorflow as tf
import numpy as np
import csv
import AnalysisModule as Ass
import datetime
from matplotlib import pyplot as plt
import ExtractData as ED
import yfinance as yf

CategoryTest = False

list_of_values_for_predicted = []
list_of_dates_for_predicted = []

if CategoryTest is False:
    csvwriter = csv.writer(open('dataset_predicted.csv', 'w'), delimiter=',', lineterminator='\n',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
    input_data = []
    result = []

    verification_reader = csv.reader(open("dataset_verification.csv"), delimiter=',', quotechar='|')
    input_data_corresponding_company = []
    dates_list_validation = []

    for row in reader:
        week = ([float(x) for x in row])
        input_data.append([week[1:]])
        result.append(week[:1])

    for row in verification_reader:
        input_data_corresponding_company.append(row[0])
        dates_list_validation.append(row[1])

    input_data = np.array(input_data)
    result = np.array(result)
    print(np.shape(input_data))

    model = tf.keras.models.load_model("SavedModels/BestPredictionModel.h5")

    print(model.summary())
    check_index = 90
    value = result[check_index]/input_data[check_index][0][0]
    predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0][0]
    print("Ratio between the value and predicted value is {}, "
          "with {} as value and {} as predicted value".format(value/predicted_value, value, predicted_value))

    invested_sum = 0
    return_sum = 100
    list_of_trades = []
    succesfull_cases = 0
    wrong_cases = 0
    succesfull_cases_1_2 = 0
    wrong_cases_1_2 = 0

    for check_index in range(int(0.8*len(input_data)) + 1, int(1*len(input_data))):
        value = result[check_index][0] / input_data[check_index][0][0]
        predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
        if predicted_value[0][0] > 2.5:
            continue
        if predicted_value[0][0] > 1.2 and invested_sum < 1500:
            invested_sum += 100
            return_sum *= value
            list_of_trades.append([predicted_value[0][0], value, check_index])

        if 2.5 > predicted_value > 1.2 and value > 1:
            succesfull_cases += 1
            plt.plot(datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"), value, "o")
            weekly = yf.download(tickers=input_data_corresponding_company[check_index], interval="1wk")
            [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"))
            list_to_be_saved = validation + price + volume
            if len(list_to_be_saved) == 103:
                csvwriter.writerow(list_to_be_saved)
            if value > 3:
                value = 3
            print("Traded " + input_data_corresponding_company[check_index] + " on " +
                  dates_list_validation[check_index])
            list_of_values_for_predicted.append(value-1)
            list_of_dates_for_predicted.append(dates_list_validation[check_index])
        elif 2.5 > predicted_value > 1.2 and value < 1:
            plt.plot(datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"),
                     value, "o")
            weekly = yf.download(tickers=input_data_corresponding_company[check_index], interval="1wk")
            [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"))
            list_to_be_saved = validation + price + volume
            if len(list_to_be_saved) == 103:
                csvwriter.writerow(list_to_be_saved)
            list_of_values_for_predicted.append(value-1)
            list_of_dates_for_predicted.append(dates_list_validation[check_index])
            wrong_cases += 1

        if 2.5 > predicted_value > 1.2 and value > 1.1:
            succesfull_cases_1_2 += 1
        elif 2.5 > predicted_value > 1.2 and value < 1.1:
            wrong_cases_1_2 += 1

        if check_index % 1000 == 0 and succesfull_cases != 0:
            print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}%"
                  "".format(succesfull_cases, wrong_cases,
                            round(100*(succesfull_cases/(succesfull_cases + wrong_cases)), 2)))

    print("Invested sum was 100 and returned sum was {} with {} trades".format(round(return_sum, 1),
                                                                               int(invested_sum/100)))
    print(list_of_trades)
    print("There were {} succesful guesses and {} wrong guesses with an accuracy of "
          "{}".format(succesfull_cases, wrong_cases, succesfull_cases/(succesfull_cases+wrong_cases)))
    print("For anything between 1.2 and 2 growth prediction were {} succesful guesses and {} wrong guesses with an "
          "accuracy of {}".format(succesfull_cases_1_2, wrong_cases_1_2,
                                  round(100*(succesfull_cases_1_2/(succesfull_cases_1_2+wrong_cases_1_2)), 2)))
    plt.show()

if CategoryTest is True:
    csvwriter = csv.writer(open('dataset_predicted_cat.csv', 'w'), delimiter=',', lineterminator='\n',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
    input_data = []
    result = []
    original_result = []

    verification_reader = csv.reader(open("dataset_verification.csv"), delimiter=',', quotechar='|')
    input_data_corresponding_company = []
    dates_list_validation = []

    for row in reader:
        week = ([float(x) for x in row])
        input_data.append([week[1:]])
        result.append(Ass.ClassifyResults(week[0] / week[1]))
        original_result.append(week[0])

    for row in verification_reader:
        input_data_corresponding_company.append(row[0])
        dates_list_validation.append(row[1])

    model = tf.keras.models.load_model("SavedModels/BestCategoryModel.h5")

    print(model.summary())

    check_index = 222222
    predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
    print(predicted_value[0])
    print([int(round(x)) for x in predicted_value[0]])
    print(Ass.Decode(predicted_value[0]))
    print(original_result[check_index])

    succesfull_cases = 0
    wrong_cases = 0
    succesfull_cases_1_2 = 0
    wrong_cases_1_2 = 0
    invested_sum = 0
    return_sum = 100
    list_of_trades = []

    cases_over_2 = 0
    cases_1_2 = 0
    cases_0_8 = 0
    cases_below_0_8 = 0

    for check_index in range(int(0.8 * len(input_data)) + 1, len(input_data)):
        value = original_result[check_index] / input_data[check_index][0][0]
        predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
        if Ass.Decode(predicted_value[0]) >= 1 and invested_sum < 1500:
            invested_sum += 100
            return_sum *= value
            list_of_trades.append([Ass.Decode(predicted_value[0]), value, check_index])

        predicted_value_numeric = Ass.Decode(predicted_value[0])

        if predicted_value_numeric == 2:
            cases_over_2 += 1
            if value < 3:
                plt.plot(datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"),
                         value, "o")
                weekly = yf.download(tickers=input_data_corresponding_company[check_index], interval="1wk")
                [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, datetime.datetime.strptime(
                    dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"))
                list_to_be_saved = validation + price + volume
                if len(list_to_be_saved) == 103:
                    csvwriter.writerow(list_to_be_saved)
                list_of_values_for_predicted.append(value-1)
                list_of_dates_for_predicted.append(dates_list_validation[check_index])
        elif predicted_value_numeric == 1.2:
            cases_1_2 += 1
            if value < 3:
                plt.plot(datetime.datetime.strptime(dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"),
                         value, "o")
                weekly = yf.download(tickers=input_data_corresponding_company[check_index], interval="1wk")
                [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, datetime.datetime.strptime(
                    dates_list_validation[check_index], "%Y-%m-%d %H:%M:%S"))
                list_to_be_saved = validation + price + volume
                if len(list_to_be_saved) == 103:
                    csvwriter.writerow(list_to_be_saved)
                list_of_values_for_predicted.append(value-1)
                list_of_dates_for_predicted.append(dates_list_validation[check_index])
        elif predicted_value_numeric == 0.8:
            cases_0_8 += 1
        elif predicted_value_numeric == 0.2:
            cases_below_0_8 += 1

        if predicted_value_numeric >= 1 and value > 1:
            succesfull_cases += 1
        elif predicted_value_numeric >= 1 > value:
            wrong_cases += 1

        if predicted_value_numeric >= 1 and value > 1.1:
            succesfull_cases_1_2 += 1
        elif predicted_value_numeric >= 1 and value < 1.1:
            wrong_cases_1_2 += 1

        if check_index % 1000 == 0 and succesfull_cases != 0:
            print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}%"
                  "".format(succesfull_cases, wrong_cases,
                            round(100 * (succesfull_cases / (succesfull_cases + wrong_cases)), 2)))

    print("Invested sum was 100 and returned sum was {} with {} trades".format(round(return_sum, 1),
                                                                               int(invested_sum / 100)))
    print(list_of_trades)
    print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}"
          "".format(succesfull_cases, wrong_cases, succesfull_cases / (succesfull_cases + wrong_cases)))
    print("For anything between 1.2 and 2 growth prediction were {} succesful guesses and {} wrong guesses with an "
          "accuracy of {}".format(succesfull_cases_1_2, wrong_cases_1_2,
                                  succesfull_cases_1_2 / (succesfull_cases_1_2 + wrong_cases_1_2)))
    plt.show()

list_of_values_for_predicted = [100*x for x in list_of_values_for_predicted]
list_of_dates_for_predicted = [datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in list_of_dates_for_predicted]

print("Average gain is: " + str(np.average(list_of_values_for_predicted)))
print("Standard deviation is: " + str(np.std(list_of_values_for_predicted)) + "%")
