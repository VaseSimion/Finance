import numpy as np
import tulipy as ti
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# looks for a rise in the mach histogram and a positive zero crossing between the last 2 values
def macd_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9

    if macdhistogram[-1] > 0 > macdhistogram[-2] and \
            macdhistogram[-1] >= macdhistogram[-2] >= macdhistogram[-3] >= macdhistogram[-4]:
        return True
    else:
        return False


# looks for a rise in the mach histogram and a negative zero crossing between the last 2 values
def macd_potential_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 12, 26, 9)  # for sell signals it should be 12, 26, 9

    if macdhistogram[-1] < 0 < macdhistogram[-2] and \
            macdhistogram[-1] <= macdhistogram[-2] <= macdhistogram[-3] <= macdhistogram[-4]:
        return True
    else:
        return False


def sma_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 17)
    if sma[-50] < sma[-5] < sma[-1] < closing_price_list[-1] and closing_price_list[-2] < sma[-2]:
        return True
    else:
        return False


def sma_potential_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 26)
    if sma[-50] > sma[-5] > sma[-1] > closing_price_list[-1] and closing_price_list[-2] > sma[-2]:
        return True
    else:
        return False


# checks if today is a positive value
def is_today_rising(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    if current_value >= open_value:
        return True
    else:
        return False


# checks if today is a negative value
def is_today_falling(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    if current_value <= open_value:
        return True
    else:
        return False


# checks if the last sma is bigger than the one before it and also that the last two lows are in ascending value
def is_stock_rising(stock):
    minimlist = return_last_minimums_buy(stock)[0]
    if minimlist[0] > minimlist[1] > minimlist[2]:  # and (list_of_sma[0] > list_of_sma[1]):
        return True
    else:
        return False


# checks if the last sma is smaller than the one before it and also that the last two lows are in descending value
def is_stock_falling(stock):
    minimlist = return_last_minimums_sell(stock)[0]
    if minimlist[0] < minimlist[1] < minimlist[2]:  # and list_of_sma[0] < list_of_sma[1]:
        return True
    else:
        return False


# returns open close values of last day in stock
def return_open_close(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    return [open_value, current_value]


# returns open close values of first day in stock
def return_open_close_first_day(stock):
    current_value = stock['Close'].tolist()[0]
    open_value = stock['Open'].tolist()[0]
    return [open_value, current_value]


# returns the reversed latest minimums of the stock and a list of reversed sma = first element is the most current sma
def return_last_minimums_buy(stock):
    firstminim = 0
    firstindex = 0

    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 17)
    list_of_sma = list(np.flip(sma))

    minimlist = [list_of_sma[0]]
    for index, value in enumerate(list_of_sma[1:-1]):
        if value < list_of_sma[index] and value < list_of_sma[index + 2]:
            if firstminim == 0:
                firstminim = value
                firstindex = index
                minimlist.append(firstminim)
                continue
            else:
                if abs((value - firstminim) / firstminim) < 0.02 and (index - firstindex) < 10:
                    firstminim = value
                    firstindex = index
                    continue
                else:
                    firstminim = value
                    firstindex = index
                    minimlist.append(firstminim)

    return [minimlist, list_of_sma]


# returns the reversed latest minimums of the stock and a list of reversed sma = first element is the most current sma
def return_last_minimums_sell(stock):
    firstminim = 0
    firstindex = 0

    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 26)
    list_of_sma = list(np.flip(sma))

    minimlist = [list_of_sma[0]]
    for index, value in enumerate(list_of_sma[1:-1]):
        if value < list_of_sma[index] and value < list_of_sma[index + 2]:
            if firstminim == 0:
                firstminim = value
                firstindex = index
                minimlist.append(firstminim)
                continue
            else:
                if abs((value - firstminim) / firstminim) < 0.02 and (index - firstindex) < 10:
                    firstminim = value
                    firstindex = index
                    continue
                else:
                    firstminim = value
                    firstindex = index
                    minimlist.append(firstminim)

    return [minimlist, list_of_sma]


# returns the latest 10 macd histogram of the stock and closing prices for sell
def return_macd_histogram_and_closing_prices_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 12, 26, 9)  # for sell signals it should be 12, 26, 9

    return [list(macdhistogram)[-10:], closing_price_list[-10:]]


# returns the latest 10 macd histogram of the stock and closing prices for buy
def return_macd_histogram_and_closing_prices_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for sell signals it should be 12, 26, 9

    return [list(macdhistogram)[-10:], closing_price_list[-10:]]


# returns the latest 10 sma of the stock and closing prices for sell
def return_sma_and_closing_prices_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 26)
    return [list(sma)[-10:], closing_price_list[-10:]]


# returns the latest 10 sma of the stock and closing prices for buy
def return_sma_and_closing_prices_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 17)
    return [list(sma)[-10:], closing_price_list[-10:]]

#  This is how a stock looks like after gets out of the yfinance
#               Open    High     Low   Close    Volume  Dividends  Stock Splits
# Date
# 2019-03-05  110.78  110.92  109.78  110.24  19538300        0.0             0
# 2019-03-06  110.41  111.19  109.97  110.29  17687000        0.0             0
# 2019-03-07  109.95  110.09  108.44  108.95  25339000        0.0             0
# 2019-03-08  107.73  109.26  107.38  109.07  22818400        0.0             0
# 2019-03-11  109.54  111.48  109.53  111.36  26491600        0.0             0
# ...            ...     ...     ...     ...       ...        ...           ...
# 2020-02-27  163.32  167.03  157.98  158.18  93174900        0.0             0

# ****************************************************************************************
# ****************************************************************************************
# ************************This is for the long term part**********************************
# ****************************************************************************************
# ****************************************************************************************


def is_eps_rising(financialdata):
    eps = list(financialdata["EPS"])
    if len(eps) < 8:
        return False
    elif eps[4] > 0 and eps[5] > 0 and eps[0]/eps[4] >= 1.25 and eps[1]/eps[5] >= 1.25:
        return True
    elif eps[0] > 0 > eps[4] and (eps[0] - eps[4])/eps[0] >= 0.25:
        return True
    else:
        return False


def sales_are_rising(financialdata):
    sales = list(financialdata["Sales"])
    if len(sales) < 8:
        return False
    elif sales[4] > 0 and sales[0] / sales[4] >= 1.25:
        return True
    else:
        return False


def is_return_on_equity_good(financialdata):
    roe = list(financialdata["ReturnOnEquity"])
    if roe[0] > 0.15:
        return True
    else:
        return False


def is_profit_good(financialdata):
    profit = list(financialdata["ProfitMargin"])
    if profit[0] > profit[4] and profit[1] > profit[5]:
        return True
    else:
        return False


def ClassifyResults(response_ratio):
    if response_ratio > 2:
        return [1, 0, 0, 0]
    elif 2 > response_ratio > 1.2:
        return [0, 1, 0, 0]
    elif 1.2 > response_ratio > 0.8:
        return [0, 0, 1, 0]
    else:
        return [0, 0, 0, 1]


def Decode(matrix):
    matrix = [float(round(x, 1)) for x in matrix]
    if matrix.index(max(matrix)) == 0:
        return 2
    elif matrix.index(max(matrix)) == 1:
        return 1.2
    elif matrix.index(max(matrix)) == 2:
        return 0.8
    else:
        return 0.2


def calculate_score(price_prediction, category_list, supervision_list):
    total_score = 0
    if price_prediction >= 1.4:
        total_score += 5
    elif price_prediction < 1.2:
        pass
    else:
        total_score += (price_prediction - 1.2) * 25
    percentage_dif = category_list[0] + category_list[1] - category_list[2] - category_list[3]

    if percentage_dif < -40:
        pass
    elif percentage_dif > 40:
        total_score += 6
    else:
        total_score += 6 * (percentage_dif + 40) / 80

    percentage_dif = supervision_list[0] + supervision_list[1] - supervision_list[2] - supervision_list[3]

    if percentage_dif < -80:
        total_score *= 0.8
    elif percentage_dif > 80:
        total_score *= 1.2
    else:
        total_score *= (1 + 0.2 * percentage_dif / 80)

    if total_score < 0:
        return 0
    elif total_score > 10:
        return 10
    else:
        return round(total_score, 2)
