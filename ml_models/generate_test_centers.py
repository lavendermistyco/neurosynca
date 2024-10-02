import requests
import random
import csv
import os

# List of states and their main cities with lat/lng coordinates for testing centers
states_and_cities = {
    'Texas': [
        {'city': 'Houston', 'latitude': 29.7604, 'longitude': -95.3698},
        {'city': 'Dallas', 'latitude': 32.7767, 'longitude': -96.7970},
        {'city': 'Austin', 'latitude': 30.2672, 'longitude': -97.7431},
        {'city': 'San Antonio', 'latitude': 29.4241, 'longitude': -98.4936}
    ],
    'Maryland': [
        {'city': 'Baltimore', 'latitude': 39.2904, 'longitude': -76.6122},
        {'city': 'Rockville', 'latitude': 39.083997, 'longitude': -77.152758},
        {'city': 'Annapolis', 'latitude': 38.9784, 'longitude': -76.4922}
    ],
    'California': [
        {'city': 'Los Angeles', 'latitude': 34.0522, 'longitude': -118.2437},
        {'city': 'San Francisco', 'latitude': 37.7749, 'longitude': -122.4194},
        {'city': 'San Diego', 'latitude': 32.7157, 'longitude': -117.1611},
        {'city': 'Sacramento', 'latitude': 38.5816, 'longitude': -121.4944}
    ],
    'New York': [
        {'city': 'New York City', 'latitude': 40.7128, 'longitude': -74.0060},
        {'city': 'Buffalo', 'latitude': 42.8864, 'longitude': -78.8784},
        {'city': 'Albany', 'latitude': 42.6526, 'longitude': -73.7562}
    ],
    'Georgia': [
        {'city': 'Atlanta', 'latitude': 33.7490, 'longitude': -84.3880},
        {'city': 'Savannah', 'latitude': 32.0809, 'longitude': -81.0912},
        {'city': 'Augusta', 'latitude': 33.4735, 'longitude': -82.0105}
    ],
    'South Carolina': [
        {'city': 'Charleston', 'latitude': 32.7765, 'longitude': -79.9311},
        {'city': 'Columbia', 'latitude': 34.0007, 'longitude': -81.0348}
    ],
    'North Carolina': [
        {'city': 'Charlotte', 'latitude': 35.2271, 'longitude': -80.8431},
        {'city': 'Raleigh', 'latitude': 35.7796, 'longitude': -78.6382}
    ],
    'Tennessee': [
        {'city': 'Nashville', 'latitude': 36.1627, 'longitude': -86.7816},
        {'city': 'Memphis', 'latitude': 35.1495, 'longitude': -90.0490}
    ]
}

# Function to query Google Places API for testing centers (e.g., hospitals or clinics)
def get_testing_centers(lat, lng, radius=50000):
    api_key = os.getenv('GOOGLE_API_KEY')  
    if not api_key:
        raise ValueError("Google API Key not set. Set the GOOGLE_API_KEY environment variable.")

    # Query Google Places API for hospitals/clinics (which could include testing centers)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=hospital&key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return []

    data = response.json()
    centers = []

    # Extract center names, locations, and ratings (if available)
    if 'results' in data:
        for place in data['results']:
            center = {
                'name': place.get('name'),
                'address': place.get('vicinity'),
                'place_id': place.get('place_id'),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng']
            }
            centers.append(center)
    return centers

# Generate random costs based on the state and the type of testing
def generate_price(state, test_type):
    if test_type == 'Autism':
        if state in ['California', 'New York']:
            return round(random.uniform(700, 1800), 2)
        elif state in ['Maryland', 'Georgia', 'North Carolina']:
            return round(random.uniform(400, 1500), 2)
        else:
            return round(random.uniform(300, 1000), 2)
    elif test_type == 'ADHD':
        if state in ['California', 'New York']:
            return round(random.uniform(500, 1400), 2)
        elif state in ['Maryland', 'Georgia', 'North Carolina']:
            return round(random.uniform(300, 1000), 2)
        else:
            return round(random.uniform(200, 700), 2)
    elif test_type == 'General Mental Health':
        if state in ['California', 'New York']:
            return round(random.uniform(200, 1000), 2)
        elif state in ['Maryland', 'Georgia', 'North Carolina']:
            return round(random.uniform(100, 800), 2)
        else:
            return round(random.uniform(100, 500), 2)

# Generate random testing type for the center
def generate_test_type():
    return random.choice(['Autism', 'ADHD', 'General Mental Health'])

# Generate dataset for selected states using Google Places API
def generate_dataset(output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['state', 'city', 'center_name', 'address', 'latitude', 'longitude', 'testing_type', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for state, cities in states_and_cities.items():
            for city_info in cities:
                print(f"Fetching testing centers for {city_info['city']}, {state}...")
                centers = get_testing_centers(city_info['latitude'], city_info['longitude'])

                for center in centers:
                    test_type = generate_test_type()  # Randomly select the testing type
                    writer.writerow({
                        'state': state,
                        'city': city_info['city'],
                        'center_name': center['name'],
                        'address': center['address'],
                        'latitude': center['latitude'],
                        'longitude': center['longitude'],
                        'testing_type': test_type,
                        'price': generate_price(state, test_type)  # Price based on state and test type
                    })

        print(f"Data saved to {output_file}")

# Run the dataset generation
if __name__ == "__main__":
    generate_dataset('test_centers_with_types_and_prices.csv')
