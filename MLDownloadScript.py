import ExtractData as ED
from datetime import datetime
from datetime import timedelta
import csv
import DatabaseStocks as Ds
import yfinance as yf

csvwriter = csv.writer(open('dataset.csv', 'w'), delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
verification_csvwriter = csv.writer(open('dataset_verification.csv', 'w'), delimiter=',', lineterminator='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

increment = 0
listOfStocksToAnalyze = Ds.get_investing_lists()
for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 10 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
        print(stock)
        initial_date = "2006-07-22"
        last_date = "2020-04-11"
        last_date = datetime.strptime(last_date, "%Y-%m-%d")
        date = datetime.strptime(initial_date, "%Y-%m-%d")

        # get the oldest date so I don't run without data
        weekly = yf.download(tickers=stock, interval="1wk")
        if (list(weekly.index)[0] + timedelta(days=365)) > date:
            date = list(weekly.index)[0] + timedelta(days=365)

        while date < last_date:
            [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, date)
#            print("new values for: " + str(date))
#            print(price)
#            print(validation)
            if date < datetime.strptime("2019-06-15", "%Y-%m-%d"):  # this is to increment the data taken, more recent
                date = date + timedelta(days=14)
            else:
                date = date + timedelta(days=7)
            list_to_be_saved = validation + price + volume
            if len(list_to_be_saved) == 103:
                csvwriter.writerow(list_to_be_saved)
                verification_csvwriter.writerow([stock, date])
    except:
        print("something went bad")
