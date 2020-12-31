import ExtractData as Ed
from datetime import datetime
from datetime import timedelta
import csv
import DatabaseStocks as Ds
import yfinance as yf
import math
from tqdm import tqdm

# This is to write the dataset and the verification, which means dates and stocks that are downloaded for training
csvwriter = csv.writer(open('dataset_custom.csv', 'w'), delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter = csv.writer(open('dataset_verification_custom.csv', 'w'), delimiter=',', lineterminator='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

increment = 0  # this is used to show progress
listOfStocksToAnalyze = Ds.get_investing_lists()  # getting the stocks that are traded on Trading212
with tqdm(total=len(listOfStocksToAnalyze)) as pbar:
    for stock in listOfStocksToAnalyze:
        try:
            initial_date = "2019-10-11"  # date from when I start downloading data
            last_date = "2020-12-14"  # last date considered for training
            last_date = datetime.strptime(last_date, "%Y-%m-%d")
            date = datetime.strptime(initial_date, "%Y-%m-%d")

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
                list_to_be_saved = validation + price + volume
                if len(list_to_be_saved) == 103:
                    csvwriter.writerow(list_to_be_saved)
                    verification_csvwriter.writerow([stock, date + timedelta(days=-1)])
                date = date + timedelta(days=7)

            pbar.update(1)
        except:
            print("something went bad with " + stock)
            pbar.update(1)
