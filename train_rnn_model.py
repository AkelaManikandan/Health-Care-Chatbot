import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import os
import pickle

# Load dataset
df = pd.read_excel("../datasets/structured_healthcare_dataset.xlsx")

# Group symptoms by disease
disease_symptoms = df.groupby("disease")["symptoms"].apply(lambda x: ', '.join(sorted(set(x)))).reset_index()

texts = disease_symptoms['symptoms'].tolist()
labels = disease_symptoms['disease'].tolist()

# Tokenize symptoms
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X)

# Encode disease labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# Define RNN model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64))
model.add(SimpleRNN(64))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(set(y)), activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=25, verbose=1)

# Save model and tokenizer
os.makedirs("models", exist_ok=True)
model.save("models/rnn_model.h5")

with open("models/rnn_tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("models/rnn_label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ RNN model trained and saved with tokenizer and label encoder")
