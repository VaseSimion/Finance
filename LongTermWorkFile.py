import ExtractData as Ed
import DatabaseStocks as Ds
import AnalysisModule as Ass

listOfStocksToAnalyze = Ds.get_lists()
for stock in listOfStocksToAnalyze:
    financial = Ed.get_financial_data(stock)
    if Ass.is_eps_rising(financial):
        return_string = stock + " had " + str(abs(round((list(financial["EPS"])[0]/list(financial["EPS"])[4]-1)*100))) \
                        + "% increase in EPS"
        if Ass.sales_are_rising(financial):
            return_string += " confirmed by sales"
        if Ass.is_return_on_equity_good(financial):
            return_string += " confirmed by return on equity"
        if Ass.is_profit_good(financial):
            return_string += " confirmed by profit growth"
        print(return_string)
