import yfinance as yf
import numpy as np
import tulipy as ti
import GraphFunctions as Gfs
import AnalysisModule as Ass
import mplfinance as mpf


one_stock_to_analyze = "MSFT"

stock = yf.Ticker(one_stock_to_analyze).history(period="1y")

[minimlist, list_of_sma] = Ass.return_last_minimums(stock)
print(list_of_sma)
print(minimlist)
print(Ass.is_stock_rising(stock))

#mpf.plot(stock,type='candle')
StockData = yf.Ticker(one_stock_to_analyze).history(period="1y")
Gfs.draw_macd_sell(StockData, "details " + one_stock_to_analyze)
