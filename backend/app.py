import os
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

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        raw_message = data.get('message', '')
        
        if not raw_message:
            return jsonify({
                "status": "error",
                "message": "No message provided",
                "data": None
            }), 400

        if not model or not tokenizer:
            return jsonify({
                "status": "error",
                "message": "Model or Tokenizer not loaded.",
                "data": None
            }), 500

        # 1. Preprocess
        clean_text = preprocess_text(raw_message)
        
        # 2. Tokenize and Pad
        seq = tokenizer.texts_to_sequences([clean_text])
        padded = pad_sequences(seq, maxlen=MAX_LEN)
        
        # 3. Predict (prob is the Spam Probability)
        prob = float(model.predict(padded)[0][0])
        
        # 4. Mandatory Mapping
        # prediction: If spam probability ≥ 0.5 → "Spam", else "Not Spam"
        is_spam = prob >= 0.5
        prediction_label = "Spam" if is_spam else "Not Spam"
        
        # confidence: Float value between 0 and 1
        confidence = prob
        
        # confidence_percent: "0% to 100%"
        confidence_percent = f"{int(confidence * 100)}%"
        
        # risk_level mapping
        if confidence < 0.50:
            risk_level = "Low"
        elif 0.50 <= confidence <= 0.75:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # 5. Keywords
        detected_keywords = get_keywords(clean_text)
        
        response = {
            "status": "success",
            "message": "Prediction completed successfully",
            "data": {
                "prediction": prediction_label,
                "confidence": round(confidence, 4),
                "confidence_percent": confidence_percent,
                "risk_level": risk_level,
                "detected_keywords": detected_keywords
            }
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": None
        }), 500

# Load artifacts once at startup
load_artifacts()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
