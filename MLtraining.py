import tensorflow as tf
import numpy as np
from tensorflow import keras
import csv


reader = csv.reader(open('dataset - Copy.csv'), delimiter=',', quotechar='|')
input_data = []
result = []

for row in reader:
    week = ([float(x) for x in row])
    input_data.append(week[1:])
    result.append(week[:1])
    #print(week)

input_data = np.array(input_data)
result = np.array(result)
training_data = input_data[:1500]
test_data = input_data[1500:]
training_results = result[:1500]
test_results = result[1500:]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(126, activation='elu', input_dim=99)) #Dense(output_dim(also hidden wight), input_dim = input_dim)
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1)) #Activation

model.add(tf.keras.layers.Dropout(0.1, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(252, use_bias=True, activation='elu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(126, activation='elu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='adam', loss='mean_squared_logarithmic_error')

model.fit(training_data, training_results, epochs=10000)

print("evaluate")
model.evaluate(test_data, test_results)

print(model.summary())
value_to_predict = np.array([input_data[90]])
print("Initially it was {} and predicted was {}".format(result[90]/input_data[90][0],model.predict(np.array([input_data[90]]))/input_data[90][0]))
print("Initially it was {} and predicted was {}".format(result[1510]/input_data[1510][0],model.predict(np.array([input_data[1510]]))/input_data[1510][0]))
print("Initially it was {} and predicted was {}".format(result[1520]/input_data[1520][0],model.predict(np.array([input_data[1520]]))/input_data[1520][0]))
print("Initially it was {} and predicted was {}".format(result[1530]/input_data[1530][0],model.predict(np.array([input_data[1530]]))/input_data[1530][0]))
