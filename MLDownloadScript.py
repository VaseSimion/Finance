import ExtractData as ED
from datetime import datetime
from datetime import timedelta
import csv
import DatabaseStocks as Ds
import yfinance as yf
import math

csvwriter = csv.writer(open('dataset.csv', 'w'), delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter = csv.writer(open('dataset_verification.csv', 'w'), delimiter=',', lineterminator='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

csvwriter_test = csv.writer(open('dataset_test.csv', 'w'), delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter_test = csv.writer(open('dataset_verification_test.csv', 'w'), delimiter=',', lineterminator='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
increment = 0
listOfStocksToAnalyze = Ds.get_investing_lists()
for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 2 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
        print(stock)
        initial_date = "2006-07-03"
        last_date = "2020-08-01"
        test_start_date = "2019-07-06"
        last_date = datetime.strptime(last_date, "%Y-%m-%d")
        date = datetime.strptime(initial_date, "%Y-%m-%d")
        test_date = datetime.strptime(test_start_date, "%Y-%m-%d")

        # get the oldest date so I don't run without data
        weekly = yf.download(tickers=stock, interval="1wk", start=initial_date)

        for index, row in weekly.iterrows():
            if math.isnan(row["Close"]) or math.isnan(row["Volume"]):
                #print(index)
                weekly = weekly.drop([index])

        if (list(weekly.index)[0] + timedelta(days=365)) > date:
            date = list(weekly.index)[0] + timedelta(days=365)

        while date < last_date:
            [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, date)
#            print("new values for: " + str(date))
#            print(price)
#            print(validation)
            if date < datetime.strptime("2017-06-17", "%Y-%m-%d"):  # this is to increment the data taken, more recent
                date = date + timedelta(days=14)
            else:
                date = date + timedelta(days=7)

            if date < test_date:  # this is to increment the data taken, more recent
                list_to_be_saved = validation + price + volume
                if len(list_to_be_saved) == 103:
                    csvwriter.writerow(list_to_be_saved)
                    verification_csvwriter.writerow([stock, date])
            else:
                list_to_be_saved = validation + price + volume
                if len(list_to_be_saved) == 103:
                    csvwriter_test.writerow(list_to_be_saved)
                    verification_csvwriter_test.writerow([stock, date])
    except:
        print("something went bad")
