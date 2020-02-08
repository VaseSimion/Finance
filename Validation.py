import AnalysisModule as Ass
import GraphFunctions as Gfs
import yfinance as yf

weeks_list=[("2019-11-04", "2019-11-08"),("2019-11-11", "2019-11-25"),("2019-11-18", "2019-11-22"),
            ("2019-11-25", "2019-11-29"),("2019-12-09", "2019-12-13"),("2019-12-16", "2019-12-20"),
            ("2020-01-06", "2020-01-11"),("2020-01-13", "2020-01-17"),("2020-01-20", "2020-01-24"),
            ("2020-01-27", "2020-01-31")]

oneweek = [("2020-01-27", "2020-01-31")]

listOfTechStocksToAnalyze = ["AAPL", "ACIW", "ACN", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "AMD", "AMAT",
                             "ANET", "ANSS", "ARW", "ATVI", "AVGO", "AVT", "AZPN", "BA", "BABA", "BB", "BLL",
                             "BYND", "BLKB", "BR", "CDK", "CDNS", "CERN", "CHKP", "CIEN", "COMM", "COUP",
                             "CREE", "CRM", "CRUS", "CRWD", "CSCO", "CVLT", "CVNA",
                             "CY", "CYBR", "DBX", "DDD", "DDOG", "DIS", "DLB", "DOCU", "DOX", "DXC",
                             "EA", "EFX", "EQT", "F", "FB",
                             "FCEL", "FDS", "FEYE", "FIT", "FTNT", "FVRR", "G", "GE", "GLW", "GOOG", "GPRO",
                             "GRMN", "GRPN", "HIMX", "HPE", "HPQ", "IAC", "IBM",
                             "INCY", "INFO", "INTC", "IPGP", "IT", "JBL", "JCOM", "JD", "KEX", "KO", "LOGI",
                             "MA", "MCHP", "MSFT", "MCD", "MCO", "MDB", "MDRX", "MOMO", "MSCI", "MSI", "MU", "NCR",
                             "NFLX", "NIO", "NKE", "NLOK", "NLSN", "NOW", "NUAN",
                             "NVDA", "NTAP", "NTGR",  "NXPI", "OKTA", "ON", "PANW", "PAYX", "PBI",
                             "PCG", "PFPT", "PING", "PTC", "PINS", "QCOM", "ORCL", "QRVO", "OTEX", "ROKU", "SABR",
                             "SHOP", "SNAP", "SPCE", "SPGI", "SPLK", "SPOT", "SQ", "SSNC",
                             "STM", "STX", "SYY", "SWKS", "TEAM", "TER", "TEVA", "TLND",
                             "TSLA", "TSM", "TTWO", "TWLO", "TWTR", "UBER", "ULTA", "UPS",
                             "V", "VEEV", "VLO", "VMW", "VRSK", "VSAT", "VZ",
                             "WB", "WDC", "WIX", "WORK", "ZM", "XRX", "ZBRA", "ZEN", "ZNGA", "ZS"]


profit_10_saptamani = 0

for period in weeks_list:
    profit = 0
    proposedbuylist = []
    proposedselllist = []
    for stock in listOfTechStocksToAnalyze:
        StockData = yf.Ticker(stock).history(start="2018"+period[0][-6:], end=period[0])
        if Ass.macd_potential_buy(StockData) and Ass.is_stock_rising(StockData):
            proposedbuylist.append(stock)
#            buy_price = Ass.return_open_close(StockData)[1]
#            CheckSellData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1])
#            [macd_temp,closing] = Ass.return_last_weeks_macd_histogram_and_closing_prices(CheckSellData)
#            profittaken = False
#            for element in macd_temp:
#                if macd<0:
#                    profit += (closing[macd_temp.index(macd)] - buy_price)/buy_price - 0.003
#                    profittaken= True
#                break
#            if not profittaken:
#                profit += (closing[-1] - buy_price)/buy_price - 0.003
            #print("Something you might wanna buy is " + stock)
            continue

        if Ass.macd_potential_sell(StockData) and Ass.is_stock_falling(StockData):
            proposedselllist.append(stock)
#            sell_price = Ass.return_open_close(StockData)[1]
#            CheckSellData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1])
#            [macd_temp,closing] = Ass.return_last_weeks_macd_histogram_and_closing_prices(CheckSellData)
#            profittaken = False
#            for element in macd_temp:
#                if macd>0:
#                    profit += (buy_price - closing[macd_temp.index(macd)])/buy_price - 0.003
#                    profittaken= True
#                break
#            if not profittaken:
#                profit += (buy_price - closing[-1])/buy_price - 0.003
#       print("Something you might wanna sell is " + stock)

    print(proposedselllist)
    print(proposedbuylist)

    for stock in proposedbuylist:
        StockData = yf.Ticker(stock).history(start=period[0], end=period[1])
        print("bought " + stock + " with " + str((Ass.return_open_close(StockData)[1]-Ass.return_open_close_first_day(StockData)[1])/Ass.return_open_close_first_day(StockData)[1]))
        profit += (Ass.return_open_close(StockData)[1]-Ass.return_open_close_first_day(StockData)[1])/Ass.return_open_close_first_day(StockData)[1]-0.003
        if profit > 0.01:
            StockData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1])
            #Gfs.draw_macd_buy(StockData, "BUY " + stock)

    for stock in proposedselllist:
        StockData = yf.Ticker(stock).history(start=period[0], end=period[1])

        print("sold " + stock + " with " + str((Ass.return_open_close(StockData)[1]-Ass.return_open_close_first_day(StockData)[1])/Ass.return_open_close_first_day(StockData)[1]))
        profit += (Ass.return_open_close(StockData)[1]-Ass.return_open_close_first_day(StockData)[1])/Ass.return_open_close_first_day(StockData)[1]-0.003
        if profit > 0.01:
            StockData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1])
            #Gfs.draw_macd_sell(StockData, "SELL " + stock)


    print("                               Profitul total al saptamanii este de {}".format(profit))
    profit_10_saptamani += profit

print("Profitul dupa 10 saptamani ar fi: {}".format(profit_10_saptamani))








