import pickle
import numpy as np
from tensorflow.keras.models import load_model

# Load RNN model
rnn_model = load_model("models/rnn_model.h5")

# Load tokenizer
with open("models/rnn_tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load label encoder
with open("models/rnn_label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load Random Forest model
with open("models/random_forest_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

# Predict disease using combined models
def predict_disease(symptoms):
    # Preprocess input: convert symptom list to symptom vector
    symptom_vector = [0] * len(tokenizer.word_index)
    for symptom in symptoms:
        idx = tokenizer.word_index.get(symptom.lower())
        if idx and idx <= len(symptom_vector):
            symptom_vector[idx - 1] = 1

    # Reshape and pad for RNN
    padded = np.array([symptom_vector])
    rnn_pred = rnn_model.predict(padded)
    rnn_result = label_encoder.inverse_transform([np.argmax(rnn_pred)])[0]

    # Random Forest expects proper symptom vector (length matches training)
    rf_symptom_vector = [1 if s in symptoms else 0 for s in tokenizer.word_index.keys()]
    rf_pred = rf_model.predict([rf_symptom_vector])[0]

    return {
        "rnn_prediction": rnn_result,
        "rf_prediction": rf_pred
    }
