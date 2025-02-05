import pandas as pd
import joblib
import os
from sklearn.neighbors import NearestNeighbors

# Define paths
DATA_PATH = "fish_dataset.csv"
MODEL_PATH = os.path.join("ml_models", "fish_recommendation.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)
print("Columns in the dataset:", df.columns)

# Check for missing values in the dataset
print("Missing values in each column:")
print(df.isnull().sum())

# Handle missing values (optional: you can also drop rows with NaNs if preferred)
df = df.fillna(0)  # Filling NaNs with 0

# Encode Hardness (Soft = 1, Medium = 2, Hard = 3)
hardness_mapping = {"Soft": 1, "Medium": 2, "Hard": 3} 
df["Hardness"] = df["Hardness"].map(hardness_mapping)

# Check for any remaining NaNs in 'Hardness' after mapping
print("Missing values in 'Hardness' column after encoding:")
print(df["Hardness"].isnull().sum())

# If there are NaNs in 'Hardness', fill them with a default value (e.g., 0)
df["Hardness"].fillna(0, inplace=True)

# Select features for training
X = df[['Min pH', 'Max pH', 'Min Temp', 'Max Temp', 'Hardness']]

# Check again for NaNs in the features
print("Missing values in feature columns:")
print(X.isnull().sum())

# Train Nearest Neighbors model
model = NearestNeighbors(n_neighbors=10, metric='euclidean')
model.fit(X)

# Save the trained model
if not os.path.exists("ml_models"):
    os.makedirs("ml_models")  # Create directory if it doesn't exist

joblib.dump(model, MODEL_PATH)

print(f"Model trained and saved successfully at {MODEL_PATH}")
