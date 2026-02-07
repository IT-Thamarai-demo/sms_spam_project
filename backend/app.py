import os
import sys
import pickle
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from config import *
from preprocessing import preprocess_text

app = Flask(__name__)

# Global variables for artifacts
model = None
tokenizer = None
tfidf_vectorizer = None

def load_artifacts():
    global model, tokenizer, tfidf_vectorizer
    print("Loading artifacts...")
    
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("Model loaded.")
    else:
        print(f"Model file not found at {MODEL_PATH}")

    if os.path.exists(TOKENIZER_PATH):
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer = pickle.load(f)
        print("Tokenizer loaded.")
    else:
        print(f"Tokenizer file not found at {TOKENIZER_PATH}")

    if os.path.exists(TFIDF_PATH):
        with open(TFIDF_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        print("TF-IDF Vectorizer loaded.")
    else:
        print(f"TF-IDF file not found at {TFIDF_PATH}")

def get_keywords(text):
    """
    Extracts keywords from the processed text using TF-IDF.
    """
    if not tfidf_vectorizer:
        return []
    
    try:
        tfidf_matrix = tfidf_vectorizer.transform([text])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        
        sorted_items = sorted(zip(tfidf_matrix.tocoo().col, tfidf_matrix.tocoo().data), 
                              key=lambda x: (x[1], x[0]), reverse=True)
        
        keywords = [feature_names[idx] for idx, score in sorted_items[:3]]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "message": "SMS Spam Detector API is running",
        "artifacts_loaded": model is not None
    })

import threading

# Global lock for prediction thread safety on Windows
prediction_lock = threading.Lock()

@app.route('/predict', methods=['POST'])
def predict():
    debug_path = r"c:\Users\Asus\Desktop\smstrain\sms_spam_project\backend\backend_debug.txt"
    try:
        data = request.get_json()
        raw_message = data.get('message', '')
        
        with open(debug_path, "a") as f:
            f.write(f"\n--- New Request: {raw_message} ---\n")
            f.flush()

        if not raw_message:
            return jsonify({"status": "error", "message": "No message", "data": None}), 400

        clean_text = preprocess_text(raw_message)
        seq = tokenizer.texts_to_sequences([clean_text])
        padded = pad_sequences(seq, maxlen=MAX_LEN)
        
        with prediction_lock:
            prob = float(model.predict(padded)[0][0])
        
        is_spam = prob >= 0.5
        prediction_label = "Spam" if is_spam else "Not Spam"
        confidence = prob
        confidence_percent = f"{int(confidence * 100)}%"
        risk_level = "High" if confidence > 0.75 else ("Medium" if confidence > 0.5 else "Low")
        
        detected_keywords = get_keywords(clean_text)
        
        return jsonify({
            "status": "success",
            "message": "Success",
            "data": {
                "prediction": prediction_label,
                "confidence": round(confidence, 4),
                "confidence_percent": confidence_percent,
                "risk_level": risk_level,
                "detected_keywords": detected_keywords
            }
        })

    except Exception as e:
        import traceback
        with open(debug_path, "a") as f:
            f.write(f"ERROR: {str(e)}\n")
            traceback.print_exc(file=f)
            f.flush()
        return jsonify({"status": "error", "message": str(e), "data": None}), 500

# Load artifacts once at startup
load_artifacts()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
