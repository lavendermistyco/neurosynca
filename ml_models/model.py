# ml_models/model.py
import tensorflow as tf
import numpy as np
import pandas as pd

def load_model():
    # Load the pre-trained deep learning model
    model = tf.keras.models.load_model('ml_models/model_weights.h5')
    return model

def predict_test_center(data):
    model = load_model()
    # Assuming you have preprocessed the data for the model
    predictions = model.predict(data)
    return predictions
