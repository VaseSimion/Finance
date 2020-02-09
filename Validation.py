import AnalysisModule as Ass
import GraphFunctions as Gfs
import yfinance as yf

weeks_list = [("2019-11-04", "2019-11-15"),("2019-11-11", "2019-11-22"),("2019-11-18", "2019-11-29"),
            ("2019-11-25", "2019-12-06"),("2019-12-02", "2019-12-13"),("2019-12-09", "2019-12-20"),
            ("2020-01-06", "2020-01-18"),("2020-01-13", "2020-01-24"),("2020-01-20", "2020-01-31"),
            ("2020-01-27", "2020-02-07")]

second_ten_weeks_list = [("2019-08-05", "2019-08-16"),("2019-08-12", "2019-08-23"),("2019-08-19", "2019-08-30"),
            ("2019-08-26", "2019-09-06"),("2019-09-02", "2019-09-13"),("2019-09-09", "2019-09-20"),
            ("2019-09-16", "2019-09-27"),("2019-09-23", "2019-10-04"),("2019-09-30", "2019-10-11"),
            ("2019-10-07", "2019-10-18")]

third_ten_week_list = [("2019-05-20", "2019-05-31"),("2019-05-27", "2019-06-07"),("2019-06-03", "2019-06-14"),
            ("2019-06-10", "2019-06-21"),("2019-06-17", "2019-06-28"),("2019-06-24", "2019-07-05"),
            ("2019-07-01", "2019-07-12"),("2019-07-08", "2019-07-19"),("2019-07-15", "2019-07-26"),
            ("2019-07-22", "2019-08-02")]


oneweek = [("2020-01-20", "2020-01-31")]

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


profit_10_saptamani = 1

for period in third_ten_week_list + second_ten_weeks_list + weeks_list:   # runs through different periods of 10 days
    average_profit = 0
    proposedbuylist = []
    proposedselllist = []
    for stock in listOfTechStocksToAnalyze:   # runs through all stocks in tech
        try:
            StockData = yf.Ticker(stock).history(start="2018"+period[0][-6:], end=period[0]) # gets history before the week I analyze
            if Ass.macd_potential_buy(StockData) and Ass.is_stock_rising(StockData):   # checks if it's a good buy
                proposedbuylist.append(stock)
                buy_price = Ass.return_open_close(StockData)[1] # saves the buy price
                CheckSellData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1]) # gets history including the period of 2 weeks
                [macd_temp,closing] = Ass.return_macd_histogram_and_closing_prices_buy(CheckSellData) # gets macd and closing
                profittaken = False
                #print(macd_temp)
                #print(closing)
                for index,macd in enumerate(macd_temp[1:]):
                    if macd < -0.2: # if the macd is at any point under 0.2 closes the transaction
                        profittaken= True
                        print("You did buy is " + stock + " at a buy price of " + str(
                            buy_price) + " and a sell price off " + str(closing[macd_temp.index(macd)]) + " due to neg macd")
                        average_profit += (1 + 5*( (closing[macd_temp.index(macd)] - buy_price)/buy_price - 0.003))
                        break

                if not profittaken: # if the macd is positive during 2 weeks waits for 10 days ot pass until it sells
                    print("You did buy is " + stock + " at a buy price of " + str(
                        buy_price) + " and a sell price off " + str(closing[-1]) + " due to 10 days")
                    average_profit += (1 + 5 * ((closing[-1] - buy_price) / buy_price - 0.003))
                #if (1 + 5*( (closing[macd_temp.index(macd)] - buy_price)/buy_price - 0.003)) < 0.9:
                #    Gfs.draw_macd_buy(CheckSellData, "BUY " + stock)

                continue

            if Ass.macd_potential_sell(StockData) and Ass.is_stock_falling(StockData): # as in the buy
                proposedselllist.append(stock)
                sell_price = Ass.return_open_close(StockData)[1]
                CheckSellData = yf.Ticker(stock).history(start="2018" + period[0][-6:], end=period[1])
                [macd_temp,closing] = Ass.return_macd_histogram_and_closing_prices_sell(CheckSellData)
                profittaken = False
                #print(macd_temp)
                #print(closing)
                for index,macd in enumerate(macd_temp[1:]):
                    if macd > 0.2:
                        profittaken= True
                        print("You did sell is " + stock + " at a sell price of " + str(sell_price) +
                              " and a buy price off " + str(closing[macd_temp.index(macd)]) + " due to pos macd")
                        average_profit += (1 + 5*((sell_price - closing[macd_temp.index(macd)])/sell_price - 0.003))
                        break

                if not profittaken:
                    print("You did sell is " + stock + " at a sell price of " + str(sell_price) +
                          " and a buy price off " + str(closing[-1]) + " due to 10 days")
                    average_profit += (1 + 5 * ((sell_price - closing[-1]) / sell_price - 0.003))
                #if (1 + 5*((sell_price - closing[macd_temp.index(macd)])/sell_price - 0.003)) < 0.9:
                #    Gfs.draw_macd_sell(CheckSellData, "SELL " + stock)

        except:
            print("stock non existent")
    print(proposedselllist)
    print(proposedbuylist)
    if len(proposedbuylist) + len(proposedselllist) >= 5:
        average_profit = average_profit / (len(proposedbuylist) + len(proposedselllist))
    elif len(proposedbuylist) + len(proposedselllist) >= 0:
        average_profit = ((5 - (len(proposedbuylist) + len(proposedselllist))) + average_profit)/5
    else:
        average_profit = 1

    print("                                                           Profitul Average per tranzactie e {}".format(
        average_profit))
    profit_10_saptamani *= (average_profit)

    print("***************************************************************" + str(period) +"*******************'Profitul dupa 10 saptamani ar fi: {}".format(profit_10_saptamani))








