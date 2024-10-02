# ml_models/model.py
import numpy as np
import pandas as pd
import joblib

def load_model():
    # Loading pre-trained model
    model = joblib.load('ml_models/random_forest_model.pkl')
    city_encoder = joblib.load('ml_models/city_encoder.pkl')
    state_encoder = joblib.load('ml_models/state_encoder.pkl')
    type_encoder = joblib.load('ml_models/type_encoder.pkl')
    return model, city_encoder, state_encoder, type_encoder

def predict_affordable_centers(model, input_features):
    # Assuming input_features is a NumPy array or similar
    predictions = model.predict(input_features)
    return predictions
