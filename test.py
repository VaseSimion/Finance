import yfinance as yf
import numpy as np
import tulipy as ti
import GraphFunctions as Gfs

one_stock_to_analyze = "INCY"

stock = yf.Ticker(one_stock_to_analyze).history(period="1y")

print(not True)

StockData = yf.Ticker("F").history(period="1y")
Gfs.draw_macd_sell(StockData, "SELL " + "F")