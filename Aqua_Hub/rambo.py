import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv('comb.csv')

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Fish Name', 'Water Type', 'Temperament', 'Size Category']
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Features and target
X = df.drop(columns=['Compatibility Score'])
y = df['Compatibility Score']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
with open('fish_compatibility.pkl', 'wb') as f:
    pickle.dump({'model': model, 'scaler': scaler, 'encoders': label_encoders}, f)

print("Model training complete and saved.")
