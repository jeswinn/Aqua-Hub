import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Load the pre-trained model
model = joblib.load("ml_models/fish_recommendation.pkl")
df = pd.read_csv("fish_dataset.csv")

# Test input
min_ph, max_ph = 7.0, 8.0
min_temp, max_temp = 22.0, 24.0
hardness = 3  # Example for 'soft'

input_data = pd.DataFrame([[min_ph, max_ph, min_temp, max_temp, hardness]], 
                          columns=['Min pH', 'Max pH', 'Min Temp', 'Max Temp', 'Hardness'])

# Get nearest neighbors
distances, indices = model.kneighbors(input_data)
recommended_fish = df.iloc[indices[0]]
print(recommended_fish)
