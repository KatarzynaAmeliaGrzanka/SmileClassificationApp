import matplotlib.pyplot as plotter_lib
import numpy as np
import PIL as image_lib
import tensorflow as tflow
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
import pathlib



image_height, image_width = 256, 256
batch_size = 32
train_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data'
validation_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data'
test_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data'
epochs = 35


train_ds = tflow.keras.preprocessing.image_dataset_from_directory(
    train_directory,
    label_mode = 'binary',
    batch_size = batch_size
)

validation_ds = tflow.keras.preprocessing.image_dataset_from_directory(
    validation_directory,
    label_mode = 'binary',
    batch_size = batch_size
)

test_ds = tflow.keras.preprocessing.image_dataset_from_directory(
    test_directory,
    label_mode = 'binary',
    batch_size = batch_size
)

resnet_model = Sequential()

pretrained_model= tflow.keras.applications.ResNet50(
    include_top=False,
    input_shape=(image_height,image_width,3),
    pooling='avg',
    classes=2,
    weights='imagenet')


for each_layer in pretrained_model.layers:
        each_layer.trainable = False

resnet_model.add(pretrained_model)
resnet_model.add(Flatten())
resnet_model.add(Dense(512, activation='relu'))
resnet_model.add(Dense(1, activation='sigmoid'))

resnet_model.compile(optimizer=Adam(lr=0.001),loss='binary_crossentropy',metrics=['accuracy'])
history = resnet_model.fit(train_ds, validation_data=validation_ds, epochs=epochs)

resnet_model.evaluate(test_ds)

converter = tflow.lite.TFLiteConverter.from_keras_model(resnet_model)
tflite_model = converter.convert()

with open("model_test.tflite", 'wb') as f:
  f.write(tflite_model)

plotter_lib.figure(figsize=(8, 8))
epochs_range = range(epochs)
plotter_lib.plot( epochs_range, history.history['accuracy'], label="Training Accuracy")
plotter_lib.plot(epochs_range, history.history['val_accuracy'], label="Validation Accuracy")
plotter_lib.axis(ymin=0.4,ymax=1)
plotter_lib.grid()
plotter_lib.title('Model Accuracy')
plotter_lib.ylabel('Accuracy')
plotter_lib.xlabel('Epochs')
plotter_lib.legend(['train', 'validation'])

plotter_lib.savefig('output-plot.png')
plotter_lib.show()




