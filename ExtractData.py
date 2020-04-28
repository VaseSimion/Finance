from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from datetime import timedelta
import math
from datetime import date


# This returns financial data that I need as a dataframe
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

        for i in range(7):
            if eps[i] == 0 and eps[i+1] == 0 and eps[i+2] == 0 and eps[i+3] == 0:
                return []
            if sales[i] == 0 and sales[i+1] == 0 and sales[i+2] == 0 and sales[i+3] == 0:
                return []
        baseline = max(max(eps),-min(eps))
        eps = [round(x/baseline,3) for x in eps]
        baseline = max(max(profit), -min(profit))
        profit = [round(x/baseline,3) for x in profit]
        baseline = max(max(sales), -min(sales))
        sales = [round(x/baseline,3) for x in sales]
        baseline = max(max(roe), -min(roe))
        roe = [round(x/baseline,3) for x in roe]

        return eps + profit + sales + roe


def get_latest_1_year_price_weekly(financialdata, date):
    dates = list(financialdata.index)
    dates.reverse()
    close_values = list(financialdata["Close"])
    close_values.reverse()
    volume = list(financialdata["Volume"])
    volume.reverse()

    while dates[0] > date and len(dates) > 12:
        dates.remove(dates[0])
        close_values.remove(close_values[0])
        volume.remove(volume[0])

    if len(close_values) < 51:
        return [[], [], []]
    close_values = close_values[:51]
    close_values = [round(x, 2) for x in close_values]
    volume = volume[:51]

    for element in close_values:
        if math.isnan(element):
            if close_values.index(element) != 0:
                close_values[close_values.index(element)] = close_values[close_values.index(element) - 1]
            else:
                close_values[close_values.index(element)] = close_values[close_values.index(element) + 1]
        else:
            continue

    for element in volume:
        if math.isnan(element):
            if volume.index(element) != 0:
                volume[volume.index(element)] = volume[volume.index(element) - 1]
            else:
                volume[volume.index(element)] = volume[volume.index(element) + 1]
        else:
            continue


    dates = list(financialdata.index)
    dates.reverse()
    close_values_validation = list(financialdata["Close"])
    close_values_validation.reverse()
    while dates[0] > date + timedelta(days=21) and len(dates) > 12:
        dates.remove(dates[0])
        close_values_validation.remove(close_values_validation[0])

    validation_values = [close_values_validation[0]]
    if math.isnan(validation_values[0]):
        value_after_3_weeks = round(close_values_validation[1], 2)
    else:
        value_after_3_weeks = round(close_values_validation[0], 2)
#    print(date)
#    print(close_values)
#    print((date + timedelta(days=21)).strftime("%Y-%m-%d"))
#    print(value_after_3_weeks)

    max_price = max(close_values+[value_after_3_weeks])
    close_values = [round(x/max_price,3) for x in close_values]
    value_after_3_weeks = round(value_after_3_weeks/max_price,3)
    max_volume = max(volume)
    volume = [round(x/max_volume,3) for x in volume]
    if 0.0 in close_values:
        return [[], [], []]
    elif math.isnan(close_values[0]) or math.isnan(value_after_3_weeks) or math.isnan(volume[0]):
        return [[], [], []]
    else:
        return [close_values, [value_after_3_weeks], volume]


def get_latest_1_year_price_weekly_from_today(financialdata):
    close_values = list(financialdata["Close"])
    close_values.reverse()
    volume = list(financialdata["Volume"])
    volume.reverse()

    if date.today().weekday() == 0 or date.today().weekday() == 5 or date.today().weekday() == 6:
        if len(close_values) < 52:
            return [[], []]
        close_values = close_values[1:52]
        close_values = [round(x, 2) for x in close_values]
        volume = volume[1:52]
    else:
        if len(close_values) < 53:
            return [[], []]
        close_values = close_values[:1] + close_values[2:52]
        close_values = [round(x, 2) for x in close_values]
        volume = volume[:1] + volume[2:52]

    for element in close_values:
        if math.isnan(element):
            if close_values.index(element) != 0:
                close_values[close_values.index(element)] = close_values[close_values.index(element) - 1]
            else:
                close_values[close_values.index(element)] = close_values[close_values.index(element) + 1]
        else:
            continue

    for element in volume:
        if math.isnan(element):
            if volume.index(element) != 0:
                volume[volume.index(element)] = volume[volume.index(element) - 1]
            else:
                volume[volume.index(element)] = volume[volume.index(element) + 1]
        else:
            continue

    max_price = max(close_values)
    close_values = [round(x/max_price,3) for x in close_values]
    max_volume = max(volume)
    volume = [round(x/max_volume,3) for x in volume]
    if 0.0 in close_values:
        return [[], []]
    elif math.isnan(close_values[0]) or math.isnan(volume[0]):
        return [[], []]
    else:
        return [close_values, volume]



def get_financial_data_for_report(stock):
    date = []
    revenue = []  # nu scrie nimic de el in carte dar mi se pare relevant
    EPS = []
    profitMargin = []
    netIncome = []  # also known as shares
    shareholderEquity = []
    url = ("https://financialmodelingprep.com/api/v3/financials/income-statement/" + stock)
    response = urlopen(url)
    results = json.loads(response.read().decode("utf-8"))

    if len(results) == 0:
        dataframeFinancialStatus = pd.DataFrame(
            np.array([revenue, EPS, profitMargin, netIncome]).transpose(),
            columns=["Revenue", "EPS", "ProfitMargin", "Sales", "ReturnOnEquity"])
        dataframeFinancialStatus.index = date
        return dataframeFinancialStatus

    for year in results["financials"]:
        date.append(year["date"])
        revenue.append(year["Revenue"])
        EPS.append(year["EPS"])
        profitMargin.append(year["Net Profit Margin"])
        netIncome.append(year["Net Income"])

    number_of_years = min(5, len(EPS))

    dataframeFinancialStatus = pd.DataFrame(
        np.array([revenue[:number_of_years], EPS[:number_of_years], profitMargin[:number_of_years],
                  netIncome[:number_of_years]]).transpose(),
        columns=["Revenue", "EPS", "ProfitMargin", "Sales"])
    dataframeFinancialStatus.index = date[:number_of_years]
#    print("done")
    return dataframeFinancialStatus