import yfinance as yf


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
