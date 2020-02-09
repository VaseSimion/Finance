import AnalysisModule as Ass
import GraphFunctions as Gfs
import yfinance as yf

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

european_stocks = ["ADS.DE", "ALO.PA", "BAYN.DE", "BMW.DE", "IFX.DE", "LHA.DE", "MAERSK-B.CO", "NOVO-B.CO",
                   "NZYM-B.CO", "SU.PA", "VWS.CO"]

proposedbuylist = []
proposedselllist = []

for stock in listOfTechStocksToAnalyze:
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
