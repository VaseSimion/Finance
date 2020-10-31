import yfinance as yf
from datetime import date
from datetime import timedelta

def write_stock(stock_performance, report_file):
    report_file.write(stock_performance.name + " at " + str(round(stock_performance.price, 2)) + "$ has " +
                      str(round(stock_performance.predicted_price_increase, 2)) +
                      " predicted as price increase and " + str(stock_performance.predicted_category_increase)
                      + " increase predicted by the category one with " +
                      str(stock_performance.predicted_category_probabilities[1]) + "%(" +
                      str(stock_performance.predicted_category_probabilities[2]) + "%)" + " as confidence and " +
                      str(stock_performance.supervised_category_prediction) + "(" +
                      str(stock_performance.supervised_probabilities[1]) + "% - " +
                      str(stock_performance.supervised_probabilities[2]) + "% as confidence)" +
                      " increase seen by the supervision model" + "\n")
    try:
        report_file.write(str(yf.Ticker(stock_performance.name).financials.iloc[[2, 6, 15]]))
    except:
        report_file.write("There was some error with getting historical data")
    report_file.write("\n")
    report_file.write("\n")


def get_list_of_3_weeks_ago():
    report_name = "Reports/ReportFile " + str(date.today() + timedelta(-21)) + ".txt"
    report_file = open(report_name, "r")
    for line in report_file:
        pass
    print(line)
    stocks_list = line.split("\",\"")
    stocks_list[0] = stocks_list[0][1:]
    stocks_list[-1] = stocks_list[-1][:-2]
    print(stocks_list)
    return stocks_list


def return_report_from_3_weeks_ago():
    zile_in_trecut = 1  # cate zile o trecut de vineri pana acum:  daca e luni ii 3
    list_of_stocks = []
    for stock in ["^GSPC"] + get_list_of_3_weeks_ago():
        try:
            weekly = yf.download(tickers=stock, interval="1d", period="6mo")
            closing = list(weekly["Close"])
            closing.reverse()
            today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]
            print(str(date.today() + timedelta(- zile_in_trecut)))
            old_day = weekly.loc[str(date.today() + timedelta(-18 - zile_in_trecut))]
            print(str(date.today() + timedelta(-18 - zile_in_trecut)))
            print(stock, str(today["Close"] / old_day["Open"]))
            list_of_stocks.append([stock, old_day["Open"], today["Close"] / old_day["Open"]])
        except:
            print("error")
    string_to_output = ""
    for element in list_of_stocks:
        string_to_output += element[0] + " bought at " + str(round(element[1], 2)) + " had an increase of " + \
                            str(round(100*(element[2] - 1), 2)) + "%\n"
    return string_to_output
