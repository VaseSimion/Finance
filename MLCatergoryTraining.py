import tensorflow as tf
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import AnalysisModule as Ass


reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
input_data = []
result = []
original_result = []
number_of_epochs = 10

for row in reader:
    week = ([float(x) for x in row])
    input_data.append([week[1:]])
    result.append(Ass.ClassifyResults(week[0]/week[1]))
    original_result.append(week[0])

input_data = np.array(input_data)
result = np.array(result)
print(np.shape(input_data))
training_data = input_data[:int(0.8*len(input_data))]
test_data = input_data[int(0.8*len(input_data)):]
training_results = result[:int(0.8*len(input_data))]
test_results = result[int(0.8*len(input_data)):]

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Reshape((25,6),input_shape=(1,150)))
model.add(tf.keras.layers.Conv1D(100, 2, padding='same', activation='linear'))
model.add(tf.keras.layers.MaxPool1D(2))
model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(252, activation='relu'))

model.add(tf.keras.layers.Dropout(0.5, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(40, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(20, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha = 0.1))

model.add(tf.keras.layers.Dense(4, activation='softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint_path = "CategoryChkp/cp.ckpt"
best_model_path = "SavedModels/BestModel.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)
model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,save_weights_only=True, verbose=1, period=5)
model_callback = tf.keras.callbacks.ModelCheckpoint(
    best_model_path, monitor='val_loss', verbose=0, save_best_only=True,
    save_weights_only=False, mode='auto', save_freq='epoch')

history = model.fit(input_data, result, validation_split=0.2, epochs=number_of_epochs,
          callbacks=[cp_callback])


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.show()

print("evaluate")
model.evaluate(test_data, test_results)

model.save("SavedModels/CategoryModel.h5")

print(model.summary())

check_index = 201500
predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
print(predicted_value[0])
print([int(round(x)) for x in predicted_value[0]])
print(Ass.Decode(predicted_value[0]))
print(original_result[check_index])

succesfull_cases = 0
wrong_cases = 0
succesfull_cases_1_2 = 0
wrong_cases_1_2 = 0
invested_sum = 0
return_sum = 100
list_of_trades = []

cases_over_2 = 0
cases_1_2 = 0
cases_0_8 = 0
cases_below_0_8 = 0

for check_index in range(int(0.8*len(input_data)) + 1, int(len(input_data)-20000)):
    value = original_result[check_index] / input_data[check_index][0][0]
    predicted_value = model.predict(np.array([input_data[check_index]])) / input_data[check_index][0][0]
    if Ass.Decode(predicted_value[0]) >= 1 and check_index < (int(0.8*len(input_data)) + 20000):
        invested_sum += 100
        return_sum *= value
        list_of_trades.append([Ass.Decode(predicted_value[0]), value, check_index])

    predicted_value_numeric = Ass.Decode(predicted_value[0])
    if predicted_value_numeric == 2:
        cases_over_2 +=1
    elif predicted_value_numeric == 1.2:
        cases_1_2 += 1
    elif predicted_value_numeric == 0.8:
        cases_0_8 += 1
    elif predicted_value_numeric == 0.2:
        cases_below_0_8 += 1

    if predicted_value_numeric >= 1 and value > 1:
        succesfull_cases += 1
    elif predicted_value_numeric >= 1 and value < 1:
        wrong_cases += 1

    if predicted_value_numeric >= 1 and value > 1.1:
        succesfull_cases_1_2 += 1
    elif predicted_value_numeric >= 1 and value < 1.1:
        wrong_cases_1_2 += 1

    if check_index%2000==0 and succesfull_cases != 0:
        print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}".format(succesfull_cases, wrong_cases, succesfull_cases/(succesfull_cases + wrong_cases)))

print("Invested sum was 100 and returned sum was {} with {} trades".format(round(return_sum,1),int(invested_sum/100)))
print(list_of_trades)
print("There were {} succesful guesses and {} wrong guesses with an accuracy of {}".format(succesfull_cases,wrong_cases,succesfull_cases/(succesfull_cases+wrong_cases)))
print("For anything between 1.2 and 2 growth prediction were {} succesful guesses and {} wrong guesses with an accuracy of {}".format(succesfull_cases_1_2,wrong_cases_1_2,succesfull_cases_1_2/(succesfull_cases_1_2+wrong_cases_1_2)))