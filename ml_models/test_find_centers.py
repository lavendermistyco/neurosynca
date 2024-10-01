import os
import sys
import pandas as pd
from find_testing_centers import load_test_centers, find_nearby_testing_centers, recommend_test_center


# test_find_centers.py
# If you encounter import issues, append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_load_centers():
    centers_df = load_test_centers()
    if centers_df is not None:
        print("Loaded Testing Centers from CSV:\n", centers_df)
    else:
        print("Test Centers CSV not found or empty.")

def test_find_nearby():
    # Test with some known location (latitude,longitude)
    location = "39.2904,76.6122"  # Baltimore, MD
    centers = find_nearby_testing_centers(location)
    
    if centers:
        print("Found Nearby Centers:\n")
        for center in centers:
            print(f"Name: {center['name']}, Address: {center['address']}")
    else:
        print("No nearby centers found.")

def test_recommend_center():
    # Example user input
    user_input = {"location": "39.2904,76.6122", "type": "Mental Health"} 
    recommended_center = recommend_test_center(user_input)
    
    if recommended_center:
        print("\nRecommended Testing Center:")
        print(f"Name: {recommended_center['name']}")
        print(f"Address: {recommended_center['address']}")
    else:
        print("No recommended center found.")

if __name__ == "__main__":
    print("Testing loading test centers from CSV:")
    test_load_centers()
    
    print("\nTesting finding nearby testing centers using Google Places API:")
    test_find_nearby()

    print("\nTesting recommending a testing center using the deep learning model:")
    test_recommend_center()
