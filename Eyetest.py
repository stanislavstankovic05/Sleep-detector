import tensorflow as tf
import keras
from keras import layers
import numpy as np
import os
from PIL import Image

def to_grayscale(x, y):
    x = tf.image.rgb_to_grayscale(x)  # Convert to (128, 128, 1)
    return x, y

# Set image size and batch size
IMG_SIZE = (128, 128)
BATCH_SIZE = 32

# Load datasets using efficient generator-based loading
train_dataset = tf.keras.utils.image_dataset_from_directory(
    "data/train",
    labels="inferred",
    label_mode="binary",
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=True
)

val_dataset = tf.keras.utils.image_dataset_from_directory(
    "data/val",  # You should separate validation data from test
    labels="inferred",
    label_mode="binary",
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=True
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    "data/test",
    labels="inferred",
    label_mode="binary",
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=False
)

# # Normalize images (rescale from 0-255 to 0-1)
# normalization_layer = layers.Rescaling(1./255)
# train_dataset = train_dataset.map(to_grayscale).map(lambda x, y: (normalization_layer(x), y))
# val_dataset = val_dataset.map(to_grayscale).map(lambda x, y: (normalization_layer(x), y))
# test_dataset = test_dataset.map(to_grayscale).map(lambda x, y: (normalization_layer(x), y))
#
#
# model_layers = [
#     tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ]
# model = tf.keras.models.Sequential(model_layers)
#
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#
# model.fit(train_dataset, validation_data=val_dataset, epochs=10, batch_size=BATCH_SIZE)
# model.save('final_model.keras')

model = tf.keras.models.load_model('final_model.keras')

loss, accuracy = model.evaluate(test_dataset)
print(f'Test accuracy: {accuracy:.4f}')