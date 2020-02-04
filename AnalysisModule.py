import numpy as np
import tulipy as ti
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def macd_potential_buy(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 8, 17, 9)  # for buy signals it should be 8,17,9

    if macdhistogram[-1] > -0.002 and macdhistogram[-1] >= macdhistogram[-3] and macdhistogram[-3] < 0.002:
        return True
    else:
        return False


def macd_potential_sell(stock):
    closing_price_list = stock['Close'].tolist()
    numpyclose = np.asarray(closing_price_list)
    macd1, macd2, macdhistogram = ti.macd(numpyclose, 12, 26, 9)  # for sell signals it should be 12, 26, 9

    if macdhistogram[-1] < 0.002 and macdhistogram[-1] <= macdhistogram[-3] and macdhistogram[-3] > 0.002:
        return True
    else:
        return False
