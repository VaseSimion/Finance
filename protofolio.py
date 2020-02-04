import GraphFunctions as Gfs
import yfinance as yf


print_yesterday = False
one_stock_to_analyze = "SPOT"
stocks_in_portofolio = ["BYND", "GRMN", "CVNA", "FB", "F", "SPOT"]

Gfs.draw_macd_buy(yf.Ticker(one_stock_to_analyze).history(period="1y"), one_stock_to_analyze)

if print_yesterday:
    for stock in stocks_in_portofolio:
        StockData = yf.Ticker(stock).history(period="1y")
        Gfs.draw_macd_buy(StockData, "BUY " + stock)
