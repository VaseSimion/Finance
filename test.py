import yfinance as yf
import numpy as np
import tulipy as ti
import GraphFunctions as Gfs
import AnalysisModule as Ass
import mplfinance as mpf


one_stock_to_analyze = "TSLA"

stock = yf.Ticker(one_stock_to_analyze).history(period="3mo", interval = "1h")
print(Ass.is_today_rising(stock))
#mpf.plot(stock,type='candle')
StockData = yf.Ticker(one_stock_to_analyze).history(period="3mo", interval = "1h")
Gfs.draw_macd_sell(StockData, "details " + one_stock_to_analyze)
