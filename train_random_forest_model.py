import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load your structured healthcare dataset
df = pd.read_excel("../datasets/structured_healthcare_dataset.xlsx")

# Get unique symptoms
all_symptoms = sorted(df['symptoms'].unique())

# Create binary symptom presence matrix for each disease
diseases = df['disease'].unique()
symptom_matrix = pd.DataFrame(0, index=diseases, columns=all_symptoms)

for _, row in df.iterrows():
    symptom_matrix.loc[row['disease'], row['symptoms']] = 1

# Reset index and split
symptom_matrix.reset_index(inplace=True)
X = symptom_matrix.drop(columns='index')
y = symptom_matrix['index']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/random_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Random Forest model trained with real data and saved to models/random_forest_model.pkl")
