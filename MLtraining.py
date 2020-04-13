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
training_data = input_data[:5000]
test_data = input_data[5000:]
training_results = result[:5000]
test_results = result[5000:]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(252, activation='elu', input_dim=99)) #Dense(output_dim(also hidden wight), input_dim = input_dim)
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4)) #Activation

#model.add(tf.keras.layers.Dropout(0.1, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(126, activation='elu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(63, activation='elu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='adam', loss='mean_absolute_percentage_error')

#log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(training_data, training_results, epochs=1000)

print("evaluate")
model.evaluate(test_data, test_results)

print(model.summary())
check_index = 90
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5001
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5002
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5003
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5004
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5100
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 5105
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
