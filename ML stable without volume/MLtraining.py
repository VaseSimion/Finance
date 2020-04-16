import tensorflow as tf
import numpy as np
from tensorflow import keras
import csv
import os

reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
input_data = []
result = []
number_of_epochs = 1

for row in reader:
    week = ([float(x) for x in row])
    input_data.append([week[1:]])
    result.append(week[:1])


input_data = np.array(input_data)
result = np.array(result)
print(np.shape(input_data))
training_data = input_data[:int(0.8*len(input_data))]
test_data = input_data[int(0.8*len(input_data)):]
training_results = result[:int(0.8*len(input_data))]
test_results = result[int(0.8*len(input_data)):]

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Reshape((33,3),input_shape=(1,99)))
model.add(tf.keras.layers.Conv1D(20, 2, padding='same', activation='linear'))
model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(252, activation='relu', input_dim=99)) #Dense(output_dim(also hidden wight), input_dim = input_dim)
#model.add(tf.keras.layers.LeakyReLU(alpha = 0)) #Activation

model.add(tf.keras.layers.Dropout(0.1, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(80, activation='linear'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(40, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(20, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(10, activation='linear'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.4))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='Adamax', loss='mean_squared_error')

checkpoint_path = "InitialTraining/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,save_weights_only=True, verbose=1, period=50)

model.fit(training_data, training_results, epochs=number_of_epochs, callbacks=[cp_callback])

print("evaluate")
model.evaluate(test_data, test_results)

print(model.summary())
check_index = 90
value = result[check_index]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))

invested_sum = 0
return_sum = 0
list_of_trades = []
succesfull_cases = 0
wrong_cases = 0
for check_index in range(int(0.8*len(input_data)) + 1, int(0.8*len(input_data) + 5000)):
    value = result[check_index][0] / input_data[check_index][0][0]
    predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
    if predicted_value[0][0] > 1.2 and check_index < int(0.8*len(input_data)) + 2000:
        invested_sum += 100
        return_sum += 100*value
        list_of_trades.append((predicted_value[0][0], value))
    if predicted_value > 1 and value > 1:
        succesfull_cases += 1
    elif predicted_value < 1 and value < 1:
        succesfull_cases += 1
    else:
        wrong_cases += 1
    if check_index%1000==0:
        print("Succesful guesses were {} and wrong cases were {} with an accuracy of {}".format(succesfull_cases, wrong_cases, succesfull_cases/(succesfull_cases + wrong_cases)))

check_index = int(0.8*len(input_data))-100
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = int(0.8*len(input_data)) - 200
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = int(0.8*len(input_data)) +100
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = int(0.8*len(input_data)) + 1
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = int(0.8*len(input_data)) + 10
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
check_index = int(0.8*len(input_data)) + 50
value = result[check_index][0]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))[0][0]/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, with {} as value and {} as predicted value".format(value/predicted_value,value,predicted_value))
print("Invested sum was {} and returned sum was {}".format(invested_sum,round(return_sum,1)))
print(list_of_trades)
print("Succesful guesses were {} and wrong cases were {} with an accuracy of {}".format(succesfull_cases,wrong_cases,succesfull_cases/(succesfull_cases+wrong_cases)))