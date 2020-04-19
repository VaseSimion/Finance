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

listOfStocksToAnalyze = Ds.get_lists()
for stock in listOfStocksToAnalyze:
    try:
        print(stock)
        initial_date = "2006-07-22"
        last_date = "2020-03-14"
        last_date = datetime.strptime(last_date, "%Y-%m-%d")
        date = datetime.strptime(initial_date, "%Y-%m-%d")

        # get the oldest date so I dont run wihtout data
        weekly = yf.download(tickers=stock, interval="1wk")
        if (list(weekly.index)[0] + timedelta(days=365)) > date:
            date = list(weekly.index)[0] + timedelta(days=365)

        financial = ED.get_financial_data(stock)

        while date < last_date:
            financial_values = ED.get_latest_3_year_quarterly(financial, date)
            [price, validation, volume] = ED.get_latest_1_year_price_weekly(weekly, date)
            print("new values for: " + str(date))
            print(financial_values)
            print(price)
            print(validation)
            if date < datetime.strptime("2019-06-15", "%Y-%m-%d"):
                date = date + timedelta(days=14)
            else:
                date = date + timedelta(days=7)
            list_to_be_saved = validation + price + volume + financial_values
            if len(list_to_be_saved) == 151:
                csvwriter.writerow(list_to_be_saved)
                verification_csvwriter.writerow([stock,date])
    except:
        print("something went bad")

#  this is how I will read my values, with the first one being the validation
# reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
# for row in reader:
#    print([float(x) for x in row])
