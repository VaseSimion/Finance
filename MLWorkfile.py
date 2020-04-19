import tensorflow as tf
import numpy as np
import os
from datetime import date
from datetime import datetime
import DatabaseStocks as Ds
import yfinance as yf
import ExtractData as Ed
import csv

prediction_file = open('predictions.csv', 'w')
prediction_writer = csv.writer(prediction_file, delimiter=',', lineterminator='\n',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Reshape((25,6),input_shape=(1,150)))
model.add(tf.keras.layers.Conv1D(25, 2, padding='same', activation='linear'))
model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(252, activation='relu'))

model.add(tf.keras.layers.Dropout(0.2, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(80, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(40, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(20, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(10, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='Adamax', loss='mean_absolute_error')

checkpoint_path = "InitialTraining/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1, period=50)

print(model.summary())

date = date.today()
prediction_writer.writerow([str(date)])
date = datetime.combine(date.today(), datetime.min.time())
increment = 0

listOfStocksToAnalyze = Ds.get_lists()
for stock in listOfStocksToAnalyze:
    increment += 1
    try:
        if increment % 50 == 0:
            print("*****************************************************************************************")
            print("                                  {} out of {}                                     ".
                  format(increment, len(listOfStocksToAnalyze)))
            print("*****************************************************************************************")
        weekly = yf.download(tickers=stock, interval="1wk", start="2019-01-11", end="2020-04-04")
        #weekly = yf.download(tickers=stock, interval="1wk", period="2y")
        financial = Ed.get_financial_data(stock)
        financial_values = Ed.get_latest_3_year_quarterly(financial, date)
        [price, volume] = Ed.get_latest_1_year_price_weekly_from_today(weekly)
        list_to_be_analyzed = price + volume + financial_values
        if len(list_to_be_analyzed) == 150:
            predicted_value = model.predict(np.array([[list_to_be_analyzed]])) / list_to_be_analyzed[0]
            prediction_writer.writerow([stock, predicted_value[0][0]])
            prediction_file.flush()
            print("{} prediction is {}".format(stock, predicted_value[0][0]))
    except:
        print("There is not enough data")
prediction_file.close()
