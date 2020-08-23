import tensorflow as tf
import numpy as np
import csv
import os
import matplotlib.pyplot as plt

reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
input_data = []
result = []
number_of_epochs = 20

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

