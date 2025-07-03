import numpy as np
import pandas as pd

# Load dataset
df = pd.read_excel("datasets/structured_healthcare_dataset.xlsx")

# Define state-action mappings (simplified version)
states = df['symptom'].unique()
actions = df['disease'].unique()

# Initialize Q-table
Q = pd.DataFrame(0, index=states, columns=actions)

# Define reward matrix (1 for matching disease-symptom, 0 otherwise)
for index, row in df.iterrows():
    Q.loc[row['symptom'], row['disease']] = 1

# Q-learning update function
def q_learning_predict(symptom):
    if symptom in Q.index:
        return Q.loc[symptom].idxmax()
    return None

print("✅ Q-learning table created (basic static implementation).")
