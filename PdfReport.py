import yfinance as yf
import GraphFunctions as Gf
import time
import pdfkit
import re


def write_start(file):
    file.write("""<!DOCTYPE html>
        <html>
        <head>
        <title>Stocks for the next 3 weeks</title>
        <style>
        table, th, td {
          border: 1px solid black;
        }
        </style>
        </head>
        <body>
        """)


def write_for_one_stock(stock, file):
    try:
        dataframe_financials = yf.Ticker(stock.name).financials.iloc[[2, 6, 15]]
        print(dataframe_financials)
        columns = [str(x)[:10]for x in list(dataframe_financials.columns)]
        income = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[0])]
        profit = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[1])]
        revenue = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[2])]
        while len(columns) < 4:
            columns.append("Nan")
            income.append("Nan")
            profit.append("Nan")
            revenue.append("Nan")

    except:
        columns = ["2020", "2019", "2018", "2017"]
        income = ["NaN", "NaN", "NaN", "NaN"]
        profit = ["NaN", "NaN", "NaN", "NaN"]
        revenue = ["NaN", "NaN", "NaN", "NaN"]

    try:
        stock_details = yf.Ticker(stock.name)
        full_name = stock_details.info["shortName"]
    except:
        full_name = stock.name

    try:
        stock_details = yf.Ticker(stock.name)
        sector = stock_details.info["sector"]
    except:
        sector = "Unknown"

    try:
        stock_details = yf.Ticker(stock.name)
        industry = stock_details.info["industry"]
    except:
        industry = "Unknown"

    Gf.save_macd_buy(yf.download(tickers=stock.name, interval="1d", period="6mo", threads=True), stock.name)
    time.sleep(2)

    file.write("""<h1>{}</h1>
    
    <p>Price is {}$ per share and volume was {} shares in the last week</p>
    <p>First script gives {} increase</p>
    <p>Second script gives {} increase and it has {}% confidence of making profit</p>
    
    
    <p><img src="C:/Users/sular/PycharmProjects/Finance/Reports/Support Files For Pdf/{}" width="800" height="600"></p>

    
    <table style="width:800px">
      <tr>
        <th></th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
      </tr>
      <tr>
        <td>Income before tax</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Gross profit</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Total revenue</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
    </table>
    <br>
    <p> It operates in the {} sector, part of the {} industry</p>
    <p> You can find more information on stock at https://finance.yahoo.com/quote/{} </p>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>""".format(full_name + " (score " + str(stock.success_score) + ")", str(round(stock.price, 2)), stock.volume,
                   str(round(stock.predicted_price_increase, 2)), stock.predicted_category_increase,
                   str(round(stock.predicted_category_probabilities[0] + stock.predicted_category_probabilities[1], 2)),
                   stock.name+".png", columns[0], columns[1], columns[2], columns[3], income[0], income[1], income[2],
                   income[3], profit[0], profit[1], profit[2], profit[3], revenue[0], revenue[1], revenue[2],
                   revenue[3], sector, industry, stock.name))


def write_results(file, results):
    list_of_results = results.split("\n")
    file.write("<h1>Results from 3 weeks ago predictions</h1>")
    for item in list_of_results:
        if "GSPC" in item:
            item = item.replace("^GSPC", "The SP500 index (which represents the market and we use it as reference)")
        file.write("<p>" + item + "</p>")

def write_end(file):
    file.write(
        """    
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <p>Disclaimer: This is just a financial experiment, I am in no position to give financial advice. I have no education in finance and you should do your investing and trading based on your own due dilligence and research.
All this recommendation should be taken with a grain a salt and a critical mind. I will invest in some of the positions mentioned above. </p>
    </body>
    </html>""")


def write_the_report(list_of_stocks, results):
    report_name = "Reports/Support Files For Pdf/Temporary.html"
    report_file = open(report_name, "w+")
    write_start(report_file)
    for stock in list_of_stocks:
        write_for_one_stock(stock, report_file)
    write_results(report_file, results)
    write_end(report_file)
    report_file.close()

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'enable-local-file-access': None}
    pdfkit.from_file('Reports\Support Files For Pdf\\Temporary.html', 'Report.pdf',
                     configuration=config, options=options)
