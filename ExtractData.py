from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from datetime import timedelta
import math


def get_financial_data(stock):
    date = []
    revenue = []  # nu scrie nimic de el in carte dar mi se pare relevant
    EPS = []
    profitMargin = []
    netIncome = []  # also known as shares
    shareholderEquity = []
    returnOnEquity = []
    url = ("https://financialmodelingprep.com/api/v3/financials/income-statement/" + stock + "?period=quarter")
    response = urlopen(url)
    results = json.loads(response.read().decode("utf-8"))

    if len(results) == 0:
        dataframeFinancialStatus = pd.DataFrame(
            np.array([revenue, EPS, profitMargin, netIncome, returnOnEquity]).transpose(),
            columns=["Revenue", "EPS", "ProfitMargin", "Sales", "ReturnOnEquity"])
        dataframeFinancialStatus.index = date
        return dataframeFinancialStatus

    for quarter in results["financials"]:
        date.append(quarter["date"])
        if quarter["Revenue"] != "":
            revenue.append(float(quarter["Revenue"]))
        else:
            revenue.append(0.0)

        if quarter["EPS"] != "":
            EPS.append(float(quarter["EPS"]))
        else:
            EPS.append(0.0)

        if quarter["Net Profit Margin"] != "":
            profitMargin.append(float(quarter["Net Profit Margin"]))
        else:
            profitMargin.append(0.0)

        if quarter["Net Income"] != "":
            netIncome.append(float(quarter["Net Income"]))
        else:
            netIncome.append(0.0)

    url = ("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + stock + "?period=quarter")
    response = urlopen(url)
    results = json.loads(response.read().decode("utf-8"))
#    print(results)
    for quarter in results["financials"]:
        if quarter["Total shareholders equity"] != "":
            shareholderEquity.append(float(quarter["Total shareholders equity"]))
        else:
            shareholderEquity.append(0.0)
    # print(shareholderEquity)

    minimumData = min(len(shareholderEquity), len(netIncome))
#    print(minimumData)
    roetuple = zip(netIncome[:minimumData], shareholderEquity[:minimumData])
    for element in roetuple:
        if element[1] == 0:
            returnOnEquity.append(-1)
        else:
            returnOnEquity.append(element[0] / element[1])
#    print(returnOnEquity)

    dataframeFinancialStatus = pd.DataFrame(
        np.array([revenue[:minimumData], EPS[:minimumData], profitMargin[:minimumData],
                  netIncome[:minimumData], returnOnEquity[:minimumData]]).transpose(),
        columns=["Revenue", "EPS", "ProfitMargin", "Sales", "ReturnOnEquity"])
    dataframeFinancialStatus.index = date[:minimumData]
#    print("done")
    return dataframeFinancialStatus


# in this function I get the values up to a specific date, and the financialdata is a dataframe with colums as above
def get_latest_3_year_quarterly(financialdata, date):
    dates = list(financialdata.index)
    eps = list(financialdata["EPS"])
    profit = list(financialdata["ProfitMargin"])
    sales = list(financialdata["Sales"])
    roe = list(financialdata["ReturnOnEquity"])
    date = date  - timedelta(days=7) # in order to compensate for yahoo giving 1 week delay of weekly data)
#    print("initial ones")
#    print(eps)
#    print(profit)
#    print(sales)
#    print(roe)
#    print(dates)

    while datetime.strptime(dates[0], "%Y-%m-%d") > date and len(dates) > 12:
        dates.remove(dates[0])
        eps.remove(eps[0])
        profit.remove(profit[0])
        sales.remove(sales[0])
        roe.remove(roe[0])

    if len(eps) < 12:
        return []
    else:
        eps = eps[:12]
        profit = profit[:12]
        sales = sales[:12]
        roe = roe[:12]

#        print("debug data")
        dates = dates[:12]
#        print(eps)
#        print(profit)
#        print(sales)
#        print(roe)
#        print(dates)

        baseline = max(max(eps),-min(eps))
        eps = [round(x/baseline,3) for x in eps]
        baseline = max(max(profit), -min(profit))
        profit = [round(x/baseline,3) for x in profit]
        baseline = max(max(sales), -min(sales))
        sales = [round(x/baseline,3) for x in sales]
        baseline = max(max(roe), -min(roe))
        roe = [round(x/baseline,3) for x in roe]

#        print("normalized")
#        print(eps)
#        print(profit)
#        print(sales)
#        print(roe)
#        print(dates)

        return eps + profit + sales + roe


def get_latest_1_year_price_weekly(stock, date):
    end_date = date.strftime("%Y-%m-%d")
    start_date = (date - timedelta(days=365)).strftime("%Y-%m-%d")
#    print("end date is ",end_date, "and start date", start_date)
    data = yf.download(tickers=stock, interval="1wk", start=start_date, end=end_date)
#    print(date)
#    print(data)
    close_values = list(data["Close"])
    close_values.reverse()
    if len(close_values) < 51:
        return [[], []]
    close_values = close_values[:51]
    close_values = [round(x, 2) for x in close_values]

    for element in close_values:
        if math.isnan(element):
            if close_values.index(element) != 0:
                close_values[close_values.index(element)] = close_values[close_values.index(element) - 1]
            else:
                close_values[close_values.index(element)] = close_values[close_values.index(element) + 1]
        else:
            continue

#    print(close_values)
    data = yf.download(tickers=stock, interval="1wk", start=(date + timedelta(days=14)).strftime("%Y-%m-%d"),
                       end=(date + timedelta(days=21)).strftime("%Y-%m-%d"))
#    print(data)
    validation_values = list(data["Close"])
    validation_values.reverse()
    if math.isnan(validation_values[0]):
        value_after_3_weeks = round(validation_values[1], 2)
    else:
        value_after_3_weeks = round(validation_values[0], 2)
#    print((date + timedelta(days=21)).strftime("%Y-%m-%d"))
#    print(data)
#    print(validation_values)
#    print(value_after_3_weeks)

    max_price = max(close_values+[value_after_3_weeks])

    close_values = [round(x/max_price,3) for x in close_values]
    value_after_3_weeks = round(value_after_3_weeks/max_price,3)
    return [close_values, [value_after_3_weeks]]
