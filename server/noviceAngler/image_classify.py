import tensorflow as tf
from django.conf import settings
import os
import tensorflow as tf
import keras
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
import numpy as np

class CNN(tf.keras.Model):
  def __init__(self, input_shape, num_classes):
    super().__init__()
    self.add(tf.keras.layers.Conv2D(32, kernel_size=(3,3),
                           activation='relu',
                           strides=(1, 1),
                           padding='same',
                           input_shape=input_shape))
    self.add(tf.keras.layers.BatchNormalization())
    self.add(tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu'))
    self.add(tf.keras.layers.BatchNormalization())
    self.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
    self.add(tf.keras.layers.Dropout(0.25))
    self.add(tf.keras.layers.Flatten())
    self.add(tf.keras.layers.Dense(128, activation='relu'))
    self.add(tf.keras.layers.BatchNormalization())
    self.add(tf.keras.layers.Dropout(0.5))
    self.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

    self.compile(loss=keras.losses.categorical_crossentropy,
                 optimizer='adam',
                 metrics=['accuracy'])
  @classmethod
  def get_config(self):
    config = super(CNN, self).get_config()
    # Add any additional configuration items specific to your CNN model
    # to the 'config' dictionary
    return config
  @classmethod
  def from_config(cls, config):
    # Extract the 'name' and 'layers' parameters from the 'config' dictionary
    name = config.pop('name', None)
    layers = config.pop('layers', None)

    # Create an instance of the CNN model using the remaining parameters in 'config'
    model = cls(**config)

    # Set the 'name' and 'layers' attributes of the model if they were provided in the 'config' dictionary
    if name is not None:
        model.name = name
    if layers is not None:
        model.layers = layers

    return model


  
  
#이미지 리사이징
def resize_image(image, target_size):
    resized_image = tf.image.resize(image, target_size)
    return resized_image
  
def image_processing(image):
  # 이미지를 텐서로 변환
  image = tf.image.decode_image(image, channels=3)  # 이미지를 디코딩합니다.

  # 원하는 타겟 크기
  target_size = (100, 100)
  
  # 이미지를 리사이즈합니다.
  resized_image = resize_image(image, target_size)
  # 이미지 정규화
  normalized_image = tf.cast(resized_image, tf.float32) / 255.0
  return normalized_image

def load_model():
    keras.utils.get_custom_objects()['CNN'] = CNN
    model_path = os.path.join(settings.BASE_DIR, 'models', 'fish_model.h5')
    
    # Load the model
    # model = tf.keras.models.load_model(model_path, custom_objects={"CNN": CNN})
    model = tf.keras.models.load_model(model_path)
    print('model_path:',model_path)
    return model
