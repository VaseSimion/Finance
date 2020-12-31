import ExtractData as Ed
from datetime import datetime
from datetime import timedelta
import csv
import DatabaseStocks as Ds
import yfinance as yf
import math
from tqdm import tqdm

# This is to write the dataset and the verification, which means dates and stocks that are downloaded for training
csvwriter = csv.writer(open('dataset.csv', 'w'), delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter = csv.writer(open('dataset_verification.csv', 'w'), delimiter=',', lineterminator='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

# This is to write the dataset:test and the verification, which means dates and stocks that are downloaded for test
csvwriter_test = csv.writer(open('dataset_test.csv', 'w'), delimiter=',', lineterminator='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter_test = csv.writer(open('dataset_verification_test.csv', 'w'), delimiter=',', lineterminator='\n',
                                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
increment = 0  # this is used to show progress
listOfStocksToAnalyze = Ds.get_investing_lists()  # getting the stocks that are traded on Trading212
with tqdm(total=len(listOfStocksToAnalyze)) as pbar:
    for stock in listOfStocksToAnalyze:
        try:
            initial_date = "2006-07-03"  # date from when I start downloading data
            last_date = "2020-10-03"  # last date considered for training
            test_start_date = "2020-05-02"  # date where the training and test datasets are split
            last_date = datetime.strptime(last_date, "%Y-%m-%d")
            date = datetime.strptime(initial_date, "%Y-%m-%d")
            test_date = datetime.strptime(test_start_date, "%Y-%m-%d")

            # Download data
            weekly = yf.download(tickers=stock, interval="1wk", start=initial_date, threads=False)

            # Remove all NaN values
            for index, row in weekly.iterrows():
                if math.isnan(row["Close"]) or math.isnan(row["Volume"]):
                    weekly = weekly.drop([index])

            # Move the start date to be at least 1 year after first value downloaded
            if (list(weekly.index)[0] + timedelta(days=365)) > date:
                date = list(weekly.index)[0] + timedelta(days=365)

            # Go through all dates bi/weekly and get the scaled data
            while date < last_date:
                [price, validation, volume] = Ed.get_latest_1_year_price_weekly(weekly, date)

                if date < test_date:  # this is to save in test folder not in validation folder
                    list_to_be_saved = validation + price + volume
                    if len(list_to_be_saved) == 103:
                        csvwriter.writerow(list_to_be_saved)
                        verification_csvwriter.writerow([stock, date + timedelta(days=-1)])
                else:
                    list_to_be_saved = validation + price + volume
                    if len(list_to_be_saved) == 103:
                        csvwriter_test.writerow(list_to_be_saved)
                        verification_csvwriter_test.writerow([stock, date + timedelta(days=-1)])

                if date < datetime.strptime("2017-06-17", "%Y-%m-%d"):  # this is to increment the data taken weekly
                    date = date + timedelta(days=14)
                else:
                    date = date + timedelta(days=7)
            pbar.update(1)
        except:
            print("something went bad with " + stock)
            pbar.update(1)
