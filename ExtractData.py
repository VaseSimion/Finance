from urllib.request import urlopen
import json
import pandas as pd
import numpy as np


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

    for quarter in results["financials"]:
        date.append(quarter["date"])
        revenue.append(float(quarter["Revenue"]))
        EPS.append(float(quarter["EPS"]))
        profitMargin.append(float(quarter["Net Profit Margin"]))
        netIncome.append(float(quarter["Net Income"]))

    # print(date)
    # print(revenue)
    # print(EPS)
    # print(profitMargin)
    # print(netIncome)

    url = ("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + stock + "?period=quarter")
    response = urlopen(url)
    results = json.loads(response.read().decode("utf-8"))

    for quarter in results["financials"]:
        shareholderEquity.append(float(quarter["Total shareholders equity"]))

    # print(shareholderEquity)
    roetuple = zip(netIncome, shareholderEquity)
    for element in roetuple:
        returnOnEquity.append(element[0] / element[1])
    # print(returnOnEquity)

    dataframeFinancialStatus = pd.DataFrame(
        np.array([revenue, EPS, profitMargin, netIncome, returnOnEquity]).transpose(),
        columns=["Revenue", "EPS", "ProfitMargin", "Sales", "ReturnOnEquity"])
    dataframeFinancialStatus.index = date
    return dataframeFinancialStatus
# print(dataframeFinancialStatus)
# print(list(dataframeFinancialStatus["EPS"]))
