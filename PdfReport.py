import yfinance as yf
import GraphFunctions as Gf
import time
import pdfkit
import re
import os
from datetime import date
import pandas as pd
import numpy as np


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


def write_data_for_one_stock(file, stock):
    try:
        dataframe_financials = yf.Ticker(stock.name).financials.iloc[[2, 6, 15]]
        print(dataframe_financials)
        columns = [str(x)[:10]for x in list(dataframe_financials.columns)]
        income = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else
                  (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[0])]
        profit = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else
                  (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[1])]
        revenue = [("-" + re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) if x < 0 else
                   (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.',  str(abs(int(x))))) for x in list(dataframe_financials.iloc[2])]
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
    <p>First script gives a chance of making significant profit of {}%</p>
    <p>Second script predicts {} increase in value</p>
    
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
    <p> You can find more information on stock at <a href=https://finance.yahoo.com/quote/{}>{}</a> </p>
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
    <br>""".format(full_name + " (score " + str(stock.success_score) + ")", str(round(stock.price, 2)),
                   stock.volume,
                   str(round(stock.predicted_category_probabilities[0] + stock.predicted_category_probabilities[1], 2)),
                   str(round(100 * (stock.predicted_price_increase - 1), 2)) + "%",
                   stock.name+".png", columns[0], columns[1], columns[2], columns[3], income[0], income[1], income[2],
                   income[3], profit[0], profit[1], profit[2], profit[3], revenue[0], revenue[1], revenue[2],
                   revenue[3], sector, industry, stock.name, stock.name))


def write_results(file, results):
    list_of_results = results.split("\n")
    file.write("<h1>Results from 3 weeks ago predictions</h1>")
    for item in list_of_results:
        if "GSPC" in item:
            item = item.replace("^GSPC", "The SP500 index (which represents the market and we use it as reference)")
        file.write("<p>" + item + "</p>")


def write_dataframe(file, list_of_stocks):
    dframe = pd.DataFrame(data=np.transpose(np.array([[str(round(100 * (stock.predicted_price_increase - 1), 2))
                                                       for stock in list_of_stocks],
                                                      [str(round(stock.predicted_category_probabilities[0] +
                                                                 stock.predicted_category_probabilities[1], 2))
                                                       for stock in list_of_stocks],
                                                      [str(round(stock.price, 2)) for stock in list_of_stocks],
                                                      [stock.volume for stock in list_of_stocks],
                                                      [stock.success_score for stock in list_of_stocks]])),
                          columns=["Predicted script 1", "Predicted confidence script 2", "Price", "Volume", "Score"],
                          index=[stock.name for stock in list_of_stocks])

    file.write("<h1>Overall view on the predictions</h1>")
    file.write("<table style=\"width:800px\">")
    file.write("""
      <tr>
        <th>Ticker</th>
        <th>Predicted increase script 1</th>
        <th>Predicted confidence script 2</th>
        <th>Price</th>
        <th>Volume</th>
        <th>Score</th>
      </tr>
      """)
    for index, row in dframe.iterrows():
        file.write("""
          <tr>
            <td>{}</td>
            <td>{} %</td>
            <td>{} %</td>
            <td>{} $</td>
            <td>{}</td>
            <td>{}</td>
          </tr>
        """.format(index, row["Predicted script 1"], row["Predicted confidence script 2"],
                   row["Price"], row["Volume"], row["Score"]))
    file.write("</table>")


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
    template_file = open(report_name, "w+")
    write_start(template_file)
    for stock in list_of_stocks:
        write_data_for_one_stock(template_file, stock)
    write_dataframe(template_file, list_of_stocks)
    write_results(template_file, results)
    write_end(template_file)
    template_file.close()

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'enable-local-file-access': None}
    pdfkit.from_file('Reports\Support Files For Pdf\\Temporary.html', 'Report ' + str(date.today()) + '.pdf',
                     configuration=config, options=options)

    supportdir = "Reports/Support Files For Pdf"

    for subdir, dirs, files in os.walk(supportdir):
        for file in files:
            print(os.path.join(subdir, file))
            os.remove(os.path.join(subdir, file))
