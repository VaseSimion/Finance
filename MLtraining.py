import tensorflow as tf
import numpy as np
from tensorflow import keras
import csv
import os

reader = csv.reader(open('dataset - Copy.csv'), delimiter=',', quotechar='|')
input_data = []
result = []
number_of_epochs = 100

for row in reader:
    week = ([float(x) for x in row])
    input_data.append(week[1:])
    result.append(week[:1])
    #print(week)

input_data = np.array(input_data)
result = np.array(result)
training_data = input_data[:6500]
test_data = input_data[6500:]
training_results = result[:6500]
test_results = result[6500:]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(252, activation='relu', input_dim=99)) #Dense(output_dim(also hidden wight), input_dim = input_dim)
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4)) #Activation

#model.add(tf.keras.layers.Dropout(0.1, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(126, activation='selu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(63, activation='selu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='Adamax', loss='mean_absolute_error')

checkpoint_path = "InitialTraining/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,save_weights_only=True, verbose=1, period=100)

model.fit(training_data, training_results, epochs=number_of_epochs, callbacks=[cp_callback])

print("evaluate")
model.evaluate(test_data, test_results)

print(model.summary())
check_index = 90
value = result[check_index]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))

invested_sum = 0
return_sum = 0
list_of_trades = []
for check_index in range(6501,6800):
    value = result[check_index] / input_data[check_index][0]
    predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0]
    if predicted_value[0][0] > 1.2:
        invested_sum += 100
        return_sum += 100*value[0]
        list_of_trades.append((predicted_value[0][0], value[0]))
check_index = 6501
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 6502
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 6503
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 6504
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 6700
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = 6705
value = result[check_index][0]/input_data[check_index][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
print("Invested sum was {} and returned sum was {}".format(invested_sum,return_sum))
print(list_of_trades)