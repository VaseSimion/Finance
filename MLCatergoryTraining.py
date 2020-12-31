import tensorflow as tf
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import AnalysisModule as Ass

tf.compat.v1.disable_eager_execution()
reader = csv.reader(open('dataset.csv'), delimiter=',', quotechar='|')
reader_test = csv.reader(open('dataset_test.csv'), delimiter=',', quotechar='|')
input_data = []
result = []
input_data_test = []
result_test = []
number_of_epochs = 30

for row in reader:
    week = ([float(x) for x in row])
    input_data.append([week[1:]])
    result.append(Ass.ClassifyResults(week[0]/week[1]))

for row in reader_test:
    week = ([float(x) for x in row])
    input_data_test.append([week[1:]])
    result_test.append(Ass.ClassifyResults(week[0]/week[1]))

training_data = np.array(input_data)
training_results = np.array(result)
print(np.shape(input_data))
test_data = np.array(input_data_test)
test_results = np.array(result_test)

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Reshape((17, 6), input_shape=(1, 102)))

model.add(tf.keras.layers.Conv1D(100, 3, padding='same', activation='relu'))
model.add(tf.keras.layers.MaxPool1D(2))

model.add(tf.keras.layers.Conv1D(100, 3, padding='same', activation='relu'))
model.add(tf.keras.layers.MaxPool1D(2))

model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(252, activation='relu'))

model.add(tf.keras.layers.Dropout(0.5, noise_shape=None, seed=None))

model.add(tf.keras.layers.Dense(40, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

model.add(tf.keras.layers.Dense(20, activation='relu'))
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

model.add(tf.keras.layers.Dense(4, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint_path = "CategoryChkp/cp.ckpt"
best_model_path = "SavedModels/BestCategoryModel.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)
# model.load_weights(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1, period=5)
model_callback = tf.keras.callbacks.ModelCheckpoint(
    best_model_path, monitor='val_accuracy', verbose=0, save_best_only=True,
    save_weights_only=False, mode='auto', save_freq='epoch')

history = model.fit(training_data, training_results, validation_data=[test_data, test_results], epochs=number_of_epochs,
                    callbacks=[cp_callback, model_callback])


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
