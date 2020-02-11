import AnalysisModule as Ass
import GraphFunctions as Gfs
import yfinance as yf
import DatabaseStocks as Ds

listOfStocksToAnalyze = Ds.get_lists()

proposedbuylist = []
proposedselllist = []

for stock in listOfStocksToAnalyze:
    # print(stock)
    StockData = yf.Ticker(stock).history(period="1y")
    if Ass.macd_potential_buy(StockData) and Ass.is_stock_rising(StockData):
        proposedbuylist.append(stock)
        print("Something you might wanna buy is " + stock)
        continue

    if Ass.macd_potential_sell(StockData) and Ass.is_stock_falling(StockData):
        proposedselllist.append(stock)
        print("Something you might wanna sell is " + stock)

for stock in proposedbuylist:
    StockData = yf.Ticker(stock).history(period="1y")
    Gfs.draw_macd_buy(StockData, "BUY " + stock)

for stock in proposedselllist:
    StockData = yf.Ticker(stock).history(period="1y")
    Gfs.draw_macd_sell(StockData, "SELL " + stock)

print(proposedselllist)
print(proposedbuylist)
