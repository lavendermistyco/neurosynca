import os
import pandas as pd
import requests
import joblib
from .model import load_model, predict_affordable_centers 

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
    # Preprocess user input to convert location dtring to coordinates
    try:
        lat, lng = map(float, user_input['location'].split(','))
        service_type = user_input.get('type', 'Autism Testing')
        # Simple encoding for service type
        service_map = {
            'Autism Testing': 1,
            'ADHD Testing': 2,
            'Mental Health': 3
        }
        service_code = service_map.get(service_type, 0)
        return [[lat, lng, service_code]]
    except Exception as e:
        print(f"Error in preprocessing input: {e}")
        return [[0, 0, 0]]

# Function to use deep learning model to recommend a test center
def recommend_test_center(user_input):
    # Preprocess and load before sending it to the model
    test_centers = load_test_centers()
    if test_centers is None:
        return None
    
    preprocessed_data = preprocess_input(user_input)
    
    # Load model and make predictions
    model = load_model()
    predictions = predict_affordable_centers(model, preprocessed_data)
    
    # Assuming lower prediction indicates more affordability
    best_center_idx = predictions.argmin()
    best_center = test_centers.iloc[best_center_idx]
    return best_center.to_dict()

# Example Usage
if __name__ == "__main__":
    # Example: Load the test centers from CSV
    centers_df = load_test_centers()
    if centers_df is not None:
        print("Loaded Testing Centers from CSV:\n", centers_df)

    # Example: Find nearby centers using Google Places API
    location = "39.2904,76.6122"  # Baltimore, MD coordinates
    nearby_centers = find_nearby_testing_centers(location)
    
    if nearby_centers:
        print("\nNearby Testing Centers from Google API:")
        for center in nearby_centers:
            print(center)

    # Recommend a testing center based on user input
    user_input = {"location": "39.2904,76.6122", "type": "Mental Health"}  # Example user input
    recommended_center = recommend_test_center(user_input)
    if recommended_center:
        print("\nRecommended Testing Center:")
        print(f"Name: {recommended_center['name']}")
        print(f"Address: {recommended_center['address']}")
    else:
        print("No recommended center found.")
