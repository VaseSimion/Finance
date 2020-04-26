import ExtractData as Ed

def append_both(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " is predicted by both with " + str(stock_performance[1]) +
                      " predicted as price increase and " + str(stock_performance[2])
                      + " increase predicted by the category one with " + str(stock_performance[4]) +
                      " as confidence" + "\n")
    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")

def append_category(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " is predicted by category script as " + str(stock_performance[1]) +
                      " price increase with " + str(stock_performance[3]) + " confidence" + "\n")

    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")


def append_price_prediction(stock_performance, report_file):
    financial_dataframe = Ed.get_financial_data_for_report(stock_performance[0])

    report_file.write(stock_performance[0] + " is predicted by price script with " + str(stock_performance[1]) +
                      " price increase" + "\n")

    report_file.write(str(financial_dataframe))
    report_file.write("\n")
    report_file.write("\n")
