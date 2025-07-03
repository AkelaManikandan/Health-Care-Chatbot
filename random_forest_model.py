import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
DATASET_PATH = "datasets/structured_healthcare_dataset.xlsx"
df = pd.read_excel(DATASET_PATH)

# Prepare data
symptoms = df['symptom'].unique()
df['symptom_vector'] = df['symptom'].apply(lambda x: [1 if s == x else 0 for s in symptoms])

X = list(df['symptom_vector'])
y = df['disease']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
with open("models/random_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Random Forest model trained and saved.")
