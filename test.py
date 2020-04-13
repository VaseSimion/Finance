import ExtractData as ED
import yfinance as yf
from datetime import datetime
from datetime import timedelta
stock = "MGM"

data = yf.download(tickers=stock, interval="1wk")
print(list(data.index))
last_date = "2020-03-02"
last_date = datetime.strptime(last_date, "%Y-%m-%d")
print(list(data.index)[0]>last_date)

financial = ED.get_financial_data(stock)

#print(financial.index[0],financial.index[1],financial.index[2])
#print(list(financial["EPS"]))
from datetime import datetime
from datetime import timedelta

date_object = datetime.strptime(financial.index[0], "%Y-%m-%d")+timedelta(days=-7)

date_object = datetime.strptime("2020-03-02", "%Y-%m-%d")

#print(date_object.strftime("%Y-%m-%d"))

#print(date_object < datetime.strptime(financial.index[0], "%Y-%m-%d"))

date = date_object

financial_values = ED.get_latest_3_year_quarterly(financial, date)
[price, validation] = ED.get_latest_1_year_price_weekly(stock, date)

print(financial_values)
print(price)
print(validation)

#******************************* writing data to file
#score1 = [1,2,3,4,5]
#score2 = [3,2,3,4,5]
#import csv
#with open('dataset.csv', 'w') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=' ', lineterminator='\n',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    spamwriter.writerow(score1)
#    spamwriter.writerow(score2)

#************************************** Reading data

#reader = csv.reader(open('dataset.csv'), delimiter=' ', quotechar='|')
#for row in reader:
#    print([int(x) for x in row])