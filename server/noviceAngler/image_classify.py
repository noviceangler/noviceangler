import tensorflow as tf
import os

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
    model_path = 'app/models/my_model.h5'  # Path to your saved model file
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    return model
