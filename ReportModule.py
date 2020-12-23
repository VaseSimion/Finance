import yfinance as yf
from datetime import date
from datetime import timedelta


# This is made to write in the txt file the performance predicted by the models
def write_stock(stock_performance, report_file):
    report_file.write(stock_performance.name + " at " + str(round(stock_performance.price, 2)) + "$ has " +
                      str(round(stock_performance.predicted_price_increase, 2)) +
                      " predicted as price increase and " + str(stock_performance.predicted_category_increase)
                      + " increase predicted by second script with " +
                      str(stock_performance.predicted_category_probabilities[1]) + "%(" +
                      str(stock_performance.predicted_category_probabilities[2]) + "%)" + " as confidence\n")
    #                  and " +
    #                  str(stock_performance.supervised_category_prediction) + "(" +
    #                  str(stock_performance.supervised_probabilities[1]) + "% - " +
    #                  str(stock_performance.supervised_probabilities[2]) + "% as confidence)" +
    #                  " increase seen by the supervision model" + "\n")
    try:
        report_file.write(str(yf.Ticker(stock_performance.name).financials.iloc[[2, 6, 15]]))
    except:
        report_file.write("There was some error with getting historical data")
    report_file.write("\n")
    report_file.write("\n")


# This looks at a file saved 3 weeks ago and returns the stocks that were predicted as a list
def get_list_of_3_weeks_ago():
    report_name = "Reports/ReportFile " + str(date.today() + timedelta(-21)) + ".txt"
    report_file = open(report_name, "r")
    line = ""
    price_active = False
    cat_active = False
    stocks_list_price = []
    stocks_list_cat = []
    for line in report_file:
        if "validation purposes this is the price" in line:
            price_active = True
            continue
        if "validation purposes this is the category" in line:
            price_active = False
            cat_active = True
            continue
        if price_active and len(line) > 2:
            print(line)
            stocks_list_price = line.split("\",\"")
            stocks_list_price[0] = stocks_list_price[0][1:]
            stocks_list_price[-1] = stocks_list_price[-1][:-3]
            print(stocks_list_price)
        if cat_active and len(line) > 2:
            print(line)
            stocks_list_cat = line.split("\",\"")
            stocks_list_cat[0] = stocks_list_cat[0][1:]
            stocks_list_cat[-1] = stocks_list_cat[-1][:-2]
            print(stocks_list_cat)

    return [stocks_list_price, stocks_list_cat]


# This returns the performance over 3 weeks of the predicted stocks 3 weeks ago (monday - friday)
def return_report_from_3_weeks_ago():
    zile_in_trecut = 1  # cate zile o trecut de vineri pana acum:  daca e luni ii 3
    zile_de_la_open = 18
    list_of_stocks = []
    list_of_stocks_cat = []
    sum_of_values = 0
    stocks = 0

    try:
        weekly = yf.download(tickers="MSFT", interval="1d", period="6mo")
        old_day = weekly.loc[str(date.today() + timedelta(-zile_de_la_open - zile_in_trecut))]
        # 3 weeks ago monday is old day
    except:
        print("That monday there were no trades, considering buy on Tuesday")
        zile_de_la_open = 17

    for stock in ["^GSPC"] + get_list_of_3_weeks_ago()[0]:
        try:
            weekly = yf.download(tickers=stock, interval="1d", period="6mo")
            closing = list(weekly["Close"])
            closing.reverse()
            today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]  # last Friday is considered today
            print(str(date.today() + timedelta(- zile_in_trecut)))
            old_day = weekly.loc[str(date.today() + timedelta(-zile_de_la_open - zile_in_trecut))]  # 3 weeks ago monday is old day
            print(str(date.today() + timedelta(-zile_de_la_open - zile_in_trecut)))
            print(stock, str(today["Close"] / old_day["Open"]))
            list_of_stocks.append([stock, old_day["Open"], today["Close"] / old_day["Open"]])
            if stock != "^GSPC":
                sum_of_values = sum_of_values + today["Close"] / old_day["Open"]
                stocks += 1
        except:
            print("error")
    string_to_output = "Script 1 analysis\n"
    if len(list_of_stocks) == 0:
        sum_of_values = 1
        stocks = 1
    for element in list_of_stocks:
        if element[2] >= 1:
            string_to_output += element[0] + " bought at " + str(round(element[1], 2)) + " had an increase of " + \
                                str(round(100 * (element[2] - 1), 2)) + "%\n"
        else:
            string_to_output += element[0] + " bought at " + str(round(element[1], 2)) + " had an decrease of " + \
                                str(round(100 * (element[2] - 1), 2)) + "%\n"
    # the output of this function is a string so it can be put in the mail module easily
    string_to_output += "Average win for this period for script 1 prediction was " + \
                        str(round(100 * (sum_of_values / stocks - 1), 2)) + "%\n\n"

    sum_of_values = 0
    stocks = 0
    for stock in get_list_of_3_weeks_ago()[1]:
        try:
            weekly = yf.download(tickers=stock, interval="1d", period="6mo")
            closing = list(weekly["Close"])
            closing.reverse()
            today = weekly.loc[str(date.today() + timedelta(-zile_in_trecut))]  # last Friday is considered today
            print(str(date.today() + timedelta(- zile_in_trecut)))
            old_day = weekly.loc[str(date.today() + timedelta(-zile_de_la_open - zile_in_trecut))]  # 3 weeks ago monday is old day
            print(str(date.today() + timedelta(-zile_de_la_open - zile_in_trecut)))
            print(stock, str(today["Close"] / old_day["Open"]))
            list_of_stocks_cat.append([stock, old_day["Open"], today["Close"] / old_day["Open"]])
            if stock != "^GSPC":
                sum_of_values = sum_of_values + today["Close"] / old_day["Open"]
                stocks += 1
        except:
            print("error")
    string_to_output += "Script 2 analysis\n"
    if len(list_of_stocks_cat) == 0:
        sum_of_values = 1
        stocks = 1
    for element in list_of_stocks_cat:
        string_to_output += element[0] + " bought at " + str(round(element[1], 2)) + " had an increase of " + \
                            str(round(100 * (element[2] - 1), 2)) + "%\n"
    # the output of this function is a string so it can be put in the mail module easily
    string_to_output += "Average win for this period for script 2 prediction was " + \
                        str(round(100 * (sum_of_values / stocks - 1), 2)) + "%\n"

    return string_to_output
