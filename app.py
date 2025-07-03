from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import pyrebase
from dotenv import load_dotenv
import os
import datetime
import re
import nltk
from firebase_admin import credentials, initialize_app, db as admin_db
from models.model_loader import predict_disease
from utils.emergency_utils import is_emergency_triggered, send_emergency_sms
from utils.nlp_utils import preprocess_text
import pandas as pd
from twilio.rest import Client
import traceback
import pickle
from keras.models import load_model
import pickle


rf_model = pickle.load(open("models/random_forest_model.pkl", "rb"))
dataset = pd.read_excel("datasets/structured_healthcare_dataset.xlsx")
symptom_index = list(dataset['symptoms'].unique())

# Load environment variables
load_dotenv()

# Firebase config
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_fallback_secret")

# Initialize Firebase app
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Twilio Setup
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Load models
random_forest_model = pickle.load(open('models/random_forest_model.pkl', 'rb'))
rnn_model = load_model('models/rnn_model.h5')

# Load dataset
try:
    dataset = pd.read_csv("datasets/structured_healthcare_dataset.csv", encoding='latin1')
    print("✅ Dataset loaded successfully.")
except Exception as e:
    print("❌ Error loading dataset:", e)
    traceback.print_exc()

# Helper function to process symptoms and make predictions
def process_symptoms(user_input):
    symptom_keywords = ['fever', 'headache', 'cough', 'fatigue', 'body ache']  # Add more symptoms as needed
    symptoms = []

    for symptom in symptom_keywords:
        if symptom in user_input.lower():
            symptoms.append(1)
        else:
            symptoms.append(0)

    return symptoms

def predict_disease(symptom_list):
    input_vector = [1 if symptom in symptom_list else 0 for symptom in symptom_index]
    prediction = rf_model.predict([input_vector])[0]
    return prediction  # disease name only

# Emergency detection and SMS
def send_emergency_sms(contact_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=contact_number
        )
        print(f"Emergency message sent to {contact_number}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Basic route for the login page
@app.route('/')
def index():
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login-email']
        password = request.form['login-password']

        # Email validation regex
        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email):
            return "❌ Invalid email format. Please enter a valid email."

        try:
            # Login using Firebase authentication
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/chatbot')  # Redirect directly to the chatbot page after login
        except Exception as e:
            error = str(e)
            if "INVALID_EMAIL" in error:
                return "❌ Invalid email."
            elif "WRONG_PASSWORD" in error:
                return "❌ Incorrect password."
            else:
                return f"Login error: {error}"

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['signup-email']
        password = request.form['signup-password']

        # Email validation regex
        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email):
            return "❌ Invalid email format. Please enter a valid email."

        try:
            # Create user with email and password using Firebase authentication
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/questionnarie')  # Redirect to next page after signup
        except Exception as e:
            error = str(e)
            if "EMAIL_EXISTS" in error:
                return "Email already exists."
            elif "WEAK_PASSWORD" in error:
                return "Password is too weak."
            else:
                return f"Signup error: {error}"

    # If GET request, return the signup form
    return render_template('login.html')

@app.route('/questionnarie', methods=['GET', 'POST'])
def questionnarie():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']
        allergies = request.form['allergies']
        chronic = request.form['chronic']
        meds = request.form['medications']
        db.child("users").child(session['user'].replace(".", "_")).set({
            "height": height, "weight": weight, "gender": gender,
            "allergies": allergies, "chronic_diseases": chronic,
            "medications": meds
        })
        return redirect(url_for('chatbot'))
    return render_template('questionnarie.html')

@app.route('/chatbot', methods=['GET'])
def chatbot():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_reply():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip().lower()

        if not user_message:
            return jsonify({"response": "😕 Please type something.", "sos_triggered": False})

        emergency_keywords = ["emergency", "help", "sos", "urgent", "accident", "bleeding"]
        sos_triggered = any(word in user_message for word in emergency_keywords)

        user_id = session.get("user", "guest").replace(".", "_")

        if sos_triggered:
            try:
                print("📞 Sending emergency SMS to:", EMERGENCY_CONTACT)
                send_emergency_sms(
                    EMERGENCY_CONTACT,
                    f"🚨 Emergency Alert from {session.get('user', 'Unknown')}: {user_message}"
                )
                print("✅ SMS sent successfully.")
            except Exception as e:
                print("❌ Twilio error:", e)
                traceback.print_exc()

            db.child("chats").child(user_id).push({
                "user_message": user_message,
                "bot_response": "Emergency alert sent.",
                "sos_triggered": True,
                "timestamp": datetime.datetime.now().isoformat()
            })

            return jsonify({
                "response": "🚨 Emergency detected! SMS alert has been sent to your emergency contact.",
                "sos_triggered": True
            })

        # Basic replies
        basic_replies = {
            "hello": "Hi there! How can I help you today?",
            "hi": "Hello! What can I assist you with?",
            "how are you": "I'm doing great, thank you! How about you?",
            "thanks": "You're welcome! Let me know if you need anything else.",
            "bye": "Goodbye! Take care.",
            "help": "How can I assist you today? Feel free to ask about your symptoms or any questions!"
        }

        if user_message in ["restart", "reset", "start over"]:
            session.clear()
            return jsonify({
                "response": "🔁 Conversation reset. 🩺 What symptoms are you experiencing?",
                "sos_triggered": False
            })

        if user_message in basic_replies:
            bot_response = basic_replies[user_message]
            db.child("chats").child(user_id).push({
                "user_message": user_message,
                "bot_response": bot_response,
                "sos_triggered": False,
                "timestamp": datetime.datetime.now().isoformat()
            })
            return jsonify({"response": bot_response, "sos_triggered": False})

        # Multi-turn diagnosis flow
        if session.get("step") is None:
            session["step"] = 1
            return jsonify({"response": "🩺 What symptoms are you experiencing?", "sos_triggered": False})

        elif session["step"] == 1:
            symptom_index = set(dataset['symptom'].str.lower().unique())  # Ensure this line is defined globally or near dataset load
            symptom_words = [word for word in user_message.split() if word in symptom_index]
            if not symptom_words:
                return jsonify({"response": "🤖 I couldn't detect valid symptoms. Please try again.", "sos_triggered": False})
            session["symptoms"] = symptom_words
            session["step"] = 2
            return jsonify({"response": "🌡️ Got it. What is your current body temperature in °F?", "sos_triggered": False})

        elif session["step"] == 2:
            try:
                temperature = float(user_message.replace("°", "").replace("f", "").strip())
                session["temperature"] = temperature
                session["step"] = 3
                return jsonify({"response": "📋 Have you already been diagnosed with any disease?", "sos_triggered": False})
            except ValueError:
                return jsonify({"response": "❌ Please enter a valid temperature in °F.", "sos_triggered": False})

        elif session["step"] == 3:
            session["user_disease"] = user_message
            session["step"] = 4
            return jsonify({"response": "💬 Do you have any chronic conditions or allergies?", "sos_triggered": False})

        elif session["step"] == 4:
            session["notes"] = user_message
            session["step"] = "complete"

            symptoms = session.get("symptoms", [])
            temperature = session.get("temperature", 98.6)
            predicted_disease = predict_disease(symptoms)

            if temperature < 98.6:
                severity_level = "Normal"
            elif temperature <= 100.4:
                severity_level = "Mild"
            elif temperature <= 102:
                severity_level = "Severe"
            else:
                severity_level = "Very Severe"

            matches = dataset[
                (dataset['disease'].str.lower() == predicted_disease.lower()) &
                (dataset['severity'].str.lower() == severity_level.lower())
            ]

            if not matches.empty:
                row = matches.iloc[0]
                cause = row.get("Definition") or row.get("Cause") or row.get("description", "N/A")
                medication = row.get("Medication", "N/A")
                advice = row.get("Advice", "N/A")
                if severity_level == "Very Severe":
                    advice += " 🚑 Please consult a doctor immediately."

                bot_response = (
                    f"🩺 Based on your symptoms, you may have *{row['disease']}*\n"
                    f"📖 Definition: {cause}\n"
                    f"🔥 Severity: {row['severity']}\n"
                    f"💊 Medication: {medication}\n"
                    f"📌 Advice: {advice}\n\n"
                    f"📝 Notes: Disease you mentioned - *{session['user_disease']}*; Allergies/conditions - *{session['notes']}*"
                )
            else:
                session.clear()
                return jsonify({"response": "🤖 Something went wrong. Let's start again. 🩺 What symptoms are you experiencing?", "sos_triggered": False})

            db.child("chats").child(user_id).push({
                "user_message": user_message,
                "bot_response": bot_response,
                "sos_triggered": False,
                "timestamp": datetime.datetime.now().isoformat()
            })

            return jsonify({"response": bot_response, "sos_triggered": False})

        else:
            session.clear()
            return jsonify({"response": "🤖 Something went wrong. Let's start again. 🩺 What symptoms are you experiencing?", "sos_triggered": False})

    except Exception as e:
        print("Error in chatbot_reply:", str(e))
        traceback.print_exc()
        return jsonify({"response": "❌ Internal error occurred.", "sos_triggered": False})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = session["user"].replace(".", "_")
    chat_logs = db.child("chats").child(user_id).get().val()

    if chat_logs:
        history_list = [
            {
                "message": entry.get("user_message", ""),
                "response": entry.get("bot_response", ""),
                "timestamp": entry.get("timestamp", ""),
                "sos_triggered": entry.get("sos_triggered", False)
            }
            for entry in chat_logs.values()
        ]
        history_list.sort(key=lambda x: x["timestamp"], reverse=True)
    else:
        history_list = []

    return jsonify({"history": history_list})

@app.route("/admin/history")
def admin_history():
    all_chats = db.child("chats").get().val()
    chat_data = []

    if all_chats:
        for user_id, chats in all_chats.items():
            for entry in chats.values():
                chat_data.append({
                    "user_id": user_id,
                    "message": entry.get("user_message", ""),
                    "response": entry.get("bot_response", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "sos_triggered": entry.get("sos_triggered", False)
                })

        chat_data.sort(key=lambda x: x["timestamp"], reverse=True)

    return render_template("admin_history.html", chat_data=chat_data)

@app.route('/reset_password')
def reset_password():
    return "Password reset functionality not implemented yet."

@app.route('/reset_chat')
def reset_chat():
    session.pop("step", None)
    session.pop("symptoms", None)
    session.pop("temperature", None)
    session.pop("user_disease", None)
    session.pop("notes", None)
    return redirect(url_for('chatbot'))

if __name__ == "__main__":
    app.run(debug=True)
