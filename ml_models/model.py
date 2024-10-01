# ml_models/model.py
import tensorflow as tf
import numpy as np
import pandas as pd
import joblib

def load_model():
    # Load your pre-trained model
    model = joblib.load('ml_models/model_weights.joblib')
    return model

def predict_affordable_centers(model, input_features):
    # Assuming input_features is a NumPy array or similar
    predictions = model.predict(input_features)
    return predictions
