import tensorflow as tf
from keras.optimizers import Adam
import numpy as np

import matplotlib.pyplot as plt
import os

img_height = 256
img_width = 256
batch_size = 20

train_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data'
validation_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data'
test_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data'
epochs = 10

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_directory,
    label_mode = 'binary',
    batch_size = batch_size
)

validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
    validation_directory,
    label_mode = 'binary',
    batch_size = batch_size
)

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_directory,
    label_mode = 'binary',
    batch_size = batch_size
)
model = tf.keras.Sequential(
    [
     tf.keras.layers.Rescaling(1./255, input_shape=(256, 256, 3)),
     tf.keras.layers.Conv2D(64, 3, activation="relu"),
     tf.keras.layers.MaxPooling2D(),
     tf.keras.layers.Conv2D(64, 3, activation="relu"),
     tf.keras.layers.MaxPooling2D(),
     tf.keras.layers.Conv2D(64, 3, activation="relu"),
     tf.keras.layers.MaxPooling2D(),
     tf.keras.layers.Flatten(),
     tf.keras.layers.Dense(128, activation="relu"),
     tf.keras.layers.Dense(1, activation="sigmoid")
    ]
)



model.compile(
    optimizer=Adam(learning_rate=0.00001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)


model.fit(
    train_ds,
    validation_data = validation_ds,
    epochs = epochs
)
model.summary()
model.evaluate(test_ds)
model.save('smile_classification_model')


tf.saved_model.save(model, "saved_model")

converter = tf.lite.TFLiteConverter.from_saved_model("saved_model") # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('model_smile_classify.tflite', 'wb') as f:
  f.write(tflite_model)

