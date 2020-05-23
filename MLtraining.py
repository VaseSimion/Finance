import tensorflow as tf
import numpy as np
import csv
import os
import matplotlib.pyplot as plt

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

model.add(tf.keras.layers.Reshape((17, 6), input_shape=(1, 102)))
model.add(tf.keras.layers.Conv1D(100, 2, padding='same', activation='linear'))
model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(252, activation='relu'))

model.add(tf.keras.layers.Dropout(0.2, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(40, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

model.add(tf.keras.layers.Dense(20, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

model.add(tf.keras.layers.Dense(10, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

model.add(tf.keras.layers.Dense(1))
model.add(tf.keras.layers.Activation('linear'))

model.compile(optimizer='Adamax', loss='mean_absolute_error')

checkpoint_path = "InitialTraining/cp.ckpt"
best_model_path = "SavedModels/BestPredictionModel.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1, period=5)
model_callback = tf.keras.callbacks.ModelCheckpoint(
    best_model_path, monitor='val_loss', verbose=0, save_best_only=True,
    save_weights_only=False, mode='auto', save_freq='epoch')

history = model.fit(input_data, result, validation_split=0.2, epochs=number_of_epochs,
                    callbacks=[cp_callback, model_callback])

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(loss))

plt.plot(epochs, loss, 'r', label='Loss')
plt.plot(epochs, val_loss, 'b', label='Validation')
plt.title('Training and validation')
plt.legend(loc=0)
plt.show()

print("evaluate")
model.evaluate(test_data, test_results)

model.save("SavedModels/PricePrediction.h5")

model = tf.keras.models.load_model("SavedModels/BestPredictionModel.h5")

print(model.summary())
check_index = 90
value = result[check_index]/input_data[check_index][0][0]
predicted_value = model.predict(np.array([input_data[check_index]]))/input_data[check_index][0][0]
print("Ratio between the value and predicted value is {}, "
      "with {} as value and {} as predicted value".format(value/predicted_value, value, predicted_value))

invested_sum = 0
return_sum = 100
list_of_trades = []
succesfull_cases = 0
wrong_cases = 0
succesfull_cases_1_2 = 0
wrong_cases_1_2 = 0


for check_index in range(int(0.8*len(input_data)) + 1, int(0.8*len(input_data) + 20000)):
    value = result[check_index][0] / input_data[check_index][0][0]
    predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
    if predicted_value[0][0] > 1.8:
        continue
    if predicted_value[0][0] > 1.15 and invested_sum < 1500:
        invested_sum += 100
        return_sum *= value
        list_of_trades.append([predicted_value[0][0], value, check_index])

    if 2 > predicted_value > 1.15 and value > 1:
        succesfull_cases += 1
    elif 2 > predicted_value > 1.15 and value < 1:
        wrong_cases += 1

    if 2 > predicted_value > 1.15 and value > 1.1:
        succesfull_cases_1_2 += 1
    elif 2 > predicted_value > 1.15 and value < 1.1:
        wrong_cases_1_2 += 1

    if check_index % 1000 == 0 and succesfull_cases != 0:
        print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}%"
              "".format(succesfull_cases, wrong_cases,
                        round(100*(succesfull_cases/(succesfull_cases + wrong_cases)), 2)))


print("Invested sum was 100 and returned sum was {} with {} trades".format(round(return_sum, 1), int(invested_sum/100)))
print(list_of_trades)
print("There were {} succesful guesses and {} wrong guesses with an accuracy of "
      "{}".format(succesfull_cases, wrong_cases, succesfull_cases/(succesfull_cases+wrong_cases)))
print("For anything between 1.2 and 2 growth prediction were {} succesful guesses and {} wrong guesses with an "
      "accuracy of {}".format(succesfull_cases_1_2, wrong_cases_1_2,
                              round(100*(succesfull_cases_1_2/(succesfull_cases_1_2+wrong_cases_1_2)), 2)))
