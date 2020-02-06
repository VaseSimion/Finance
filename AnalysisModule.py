import numpy as np
import tulipy as ti
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def macd_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9

    if macdhistogram[-1] > -0.002 and macdhistogram[-1] >= macdhistogram[-3] < 0.002:
        return True
    else:
        return False


def macd_potential_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 12, 26, 9)  # for sell signals it should be 12, 26, 9

    if macdhistogram[-1] < 0.002 and macdhistogram[-1] <= macdhistogram[-3] > -0.002:
        return True
    else:
        return False


def is_today_rising(stock):
    current_value = stock['Close'].tolist()[-1]
    open_value = stock['Open'].tolist()[-1]
    if current_value > open_value:
        return True
    else:
        return False


def is_stock_rising(stock):
    minimlist = return_last_minimums(stock)
    if minimlist[0] > minimlist[1] > minimlist[2]:
        return True
    else:
        return False


def is_stock_falling(stock):
    minimlist = return_last_minimums(stock)
    if minimlist[0] < minimlist[1] < minimlist[2]:
        return True
    else:
        return False


def return_last_minimums(stock):
    firstminim = 0
    firstindex = 0

    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    sma = ti.sma(numpyclose, 7)
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
                if abs((value - firstminim) / firstminim) < 0.02 and (index - firstindex) < 15:
                    firstminim = value
                    firstindex = index
                    continue
                else:
                    firstminim = value
                    firstindex = index
                    minimlist.append(firstminim)

    return minimlist
