import ExtractData as Ed


def append_both(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " at " + str(stock_performance[2]) + "$ has " + str(stock_performance[1]) +
                      " predicted as price increase and " + str(stock_performance[3])
                      + " increase predicted by the category one with " + str(stock_performance[5]) + "(" +
                      str(stock_performance[6]) + ")" + " as confidence" + "\n")
    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")


def append_category(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " at " + str(stock_performance[2]) + "$ has " + str(stock_performance[1]) +
                      " predicted as price increase and " + str(stock_performance[3])
                      + " increase predicted by the category one with " + str(stock_performance[5]) + "(" +
                      str(stock_performance[6]) + ")" + " as confidence" + "\n")

    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")


def append_price_prediction(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " at " + str(stock_performance[2]) + "$ is predicted by price script with "
                      + str(stock_performance[1]) + " price increase" + "\n")

    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")
