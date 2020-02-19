import GraphFunctions as Gfs
import yfinance as yf
import AnalysisModule as Ass

bought_list = ["KSU"]
sold_list = []

for stock in bought_list:
    CheckSellData = yf.Ticker(stock).history(period="6mo")
    [macd_temp, closing] = Ass.return_macd_histogram_and_closing_prices_buy(CheckSellData)
    if macd_temp[-1] < -0.001:
        Gfs.draw_macd_buy(CheckSellData, "You should CLOSE " + stock)
    else:
        Gfs.draw_macd_buy(CheckSellData, "You should look at " + stock)

for stock in sold_list:
    CheckSellData = yf.Ticker(stock).history(period="6mo")
    [macd_temp, closing] = Ass.return_macd_histogram_and_closing_prices_sell(CheckSellData)
    if macd_temp[-1] > 0.001:
        Gfs.draw_macd_sell(CheckSellData, "You should CLOSE " + stock)
    else:
        Gfs.draw_macd_sell(CheckSellData, "You should look at " + stock)
