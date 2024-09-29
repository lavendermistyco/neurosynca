import os
import pandas as pd
import requests
from ml_models.model import predict_test_center  # Assuming you have a model file

# Load the test centers CSV file
def load_test_centers():
    try:
        df = pd.read_csv('ml_models/test_centers.csv')
        return df
    except FileNotFoundError:
        print("Error: test_centers.csv file not found.")
        return None

# Function to find nearby testing centers using Google Places API
def find_nearby_testing_centers(location, radius=50000):
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Google API Key not set. Make sure to set the GOOGLE_API_KEY environment variable.")
    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=hospital&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    centers = []
    if 'results' in data:
        for place in data['results']:
            center = {
                'name': place.get('name'),
                'address': place.get('vicinity'),
                'place_id': place.get('place_id'),
            }
            centers.append(center)
    return centers

# Function to preprocess input (can be customized based on your data)
def preprocess_input(user_input):
    # Preprocess user input to match the model's expected input format
    # E.g., this could include normalizing coordinates, encoding information, etc.
    return user_input

# Function to use deep learning model to recommend a test center
def recommend_test_center(user_input):
    # Preprocess input before sending it to the model
    preprocessed_data = preprocess_input(user_input)
    
    # Get the model's prediction for the best test center
    predictions = predict_test_center(preprocessed_data)
    
    # Load test centers and map predictions
    test_centers = load_test_centers()
    if test_centers is not None:
        best_center_idx = predictions.argmax()
        best_center = test_centers.iloc[best_center_idx]
        return best_center
    else:
        return "No test centers found."

# Example Usage
if __name__ == "__main__":
    # Example: Load the test centers from CSV
    centers_df = load_test_centers()
    if centers_df is not None:
        print("Loaded Testing Centers from CSV:\n", centers_df)

    # Example: Find nearby centers using Google Places API
    location = "29.4241,-98.4936"  # San Antonio, TX coordinates
    nearby_centers = find_nearby_testing_centers(location)
    
    if nearby_centers:
        print("\nNearby Testing Centers from Google API:")
        for center in nearby_centers:
            print(center)

    # Example: Recommend a testing center based on deep learning model
    user_input = {"location": location, "type": "mental_health"}  # Modify based on input requirements
    recommended_center = recommend_test_center(user_input)
    print("\nRecommended Testing Center:")
    print(recommended_center)
