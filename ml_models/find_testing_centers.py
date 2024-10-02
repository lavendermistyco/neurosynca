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

# extract city and state from Google address components
def extract_city_state(address_components):
    city = None
    state = None

    for component in address_components:
        if "locality" in component["types"]:  # Extract city
            city = component["long_name"]
        if "administrative_area_level_1" in component["types"]:  # Extract state
            state = component["short_name"]

    return city, state

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
            # Get the place_id to make a request for place details (for city, state)
            place_id = place.get('place_id')

            # Call Places Details API to get more detailed address information
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
            detail_response = requests.get(details_url)
            place_details = detail_response.json()

            if 'result' in place_details:
                address_components = place_details['result'].get('address_components', [])
                city, state = extract_city_state(address_components)
            else:
                city, state = 'default_city', 'default_state'

            # Populate center details
            center = {
                'name': place.get('name'),
                'address': place.get('vicinity'),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'city': city,
                'state': state,
                'place_id': place.get('place_id'),
            }
            centers.append(center)
    return centers

# Function to preprocess input (can be customized based on your data)
def preprocess_input(lat, lng, city, state, service_type):
    try:
        model, city_encoder, state_encoder, type_encoder = load_model()

        city_encoded = city_encoder.transform([city])[0]
        state_encoded = state_encoder.transform([state])[0]
        service_type_encoded = type_encoder.transform([service_type])[0]

        return [[lat, lng, city_encoded, state_encoded, service_type_encoded]]

    except Exception as e:
        print(f"Error in preprocessing input: {e}")
        return [[0, 0, 0, 0, 0]]  

# Function to use deep learning model to recommend a test center
def recommend_test_center(nearby_centers, service_type):
    model, city_encoder, state_encoder, type_encoder = load_model() 
    test_centers = load_test_centers()
    
    if test_centers is None or not nearby_centers:
        return None

    processed_inputs = []
    for center in nearby_centers:
        lat, lng = center['latitude'], center['longitude']
        city = center['city']  
        state = center['state']  

        processed_input = preprocess_input(lat, lng, city, state, service_type)
        processed_inputs.append(processed_input[0])

    predictions = model.predict(processed_inputs) 
    
    for i, center in enumerate(nearby_centers):
        center['predicted_price'] = predictions[i]
        center['testing_type'] = service_type
    
    nearby_centers.sort(key=lambda x: x['predicted_price'])
    
    return nearby_centers[0] if nearby_centers else None

# Example Usage
if __name__ == "__main__":
     # Example location and service type
    location = "39.2904,-76.6122"  # Baltimore, MD
    service_type = "Mental Health"

    # Find nearby centers using Google Places API
    nearby_centers = find_nearby_testing_centers(location)

    if nearby_centers:
        # Recommend the most affordable center
        recommended_center = recommend_test_center(nearby_centers, service_type)
        if recommended_center:
            print("\nRecommended Testing Center:")
            print(f"Name: {recommended_center['name']}")
            print(f"Address: {recommended_center['address']}")
            print(f"Predicted Price: ${recommended_center['predicted_price']}")
        else:
            print("No center could be recommended.")
    else:
        print("No nearby centers found.")
