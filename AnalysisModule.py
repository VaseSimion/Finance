import numpy as np
import tulipy as ti
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# looks for a rise in the mach histogram and a positive zero crossing between the last 2 values
def macd_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9

    if macdhistogram[-1] > 0.01 and macdhistogram[-1] >= macdhistogram[-2] >= macdhistogram[-3] >= macdhistogram[-4] \
            and macdhistogram[-2] < -0.01:
        return True
    else:
        return False


# looks for a rise in the mach histogram and a negative zero crossing between the last 2 values
def macd_potential_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 12, 26, 9)  # for sell signals it should be 12, 26, 9

    if macdhistogram[-1] < -0.001 and macdhistogram[-1] <= macdhistogram[-2] <= macdhistogram[-3] <= macdhistogram[-4] \
            and macdhistogram[-2] > 0.01:
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
    [minimlist, list_of_sma] = return_last_minimums_buy(stock)
    if minimlist[0] > minimlist[1] > minimlist[2] and (list_of_sma[0] > list_of_sma[1]):
        return True
    else:
        return False


# checks if the last sma is smaller than the one before it and also that the last two lows are in descending value
def is_stock_falling(stock):
    [minimlist, list_of_sma] = return_last_minimums_sell(stock)
    if minimlist[0] < minimlist[1] < minimlist[2] and list_of_sma[0] < list_of_sma[1]:
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
                if abs((value - firstminim) / firstminim) < 0.02 and (index - firstindex) < 20:
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
                if abs((value - firstminim) / firstminim) < 0.02 and (index - firstindex) < 20:
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
