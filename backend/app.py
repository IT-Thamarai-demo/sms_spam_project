import os
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

from preprocess import clean_text, tokenize_and_lemmatize
from features import texts_to_padded_sequences
from gensim.models import Word2Vec
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)  # Enable CORS for Android app requests

# Load artifacts
ART_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
ART_PATH = os.path.abspath(ART_PATH)
MODEL_PATH = os.path.join(ART_PATH, 'sms_model.h5')
TOKENIZER_PATH = os.path.join(ART_PATH, 'tokenizer.pkl')
TFIDF_PATH = os.path.join(ART_PATH, 'tfidf.pkl')
W2V_PATH = os.path.join(ART_PATH, 'word2vec.model')


def load_artifacts():
    global model, tokenizer, tfidf, w2v
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError('Model not found. Train and place models/sms_model.h5')
    model = load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)
    with open(TFIDF_PATH, 'rb') as f:
        tfidf = pickle.load(f)
    if os.path.exists(W2V_PATH):
        w2v = Word2Vec.load(W2V_PATH)
    else:
        w2v = None


def extract_keywords(text, top_k=5):
    # simple approach: return most informative tokens (by TF-IDF if available)
    cleaned = clean_text(text)
    toks = tokenize_and_lemmatize(cleaned)
    keywords = []
    for t in toks:
        if any(k in t for k in ['free', 'click', 'call', 'urgent', 'win', 'won', 'prize']):
            keywords.append(t)
    keywords = list(dict.fromkeys(keywords))[:top_k]
    return keywords


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for Android app to verify connection"""
    return jsonify({
        "status": "online",
        "message": "SMS Spam Detector API is running",
        "server_ip": "10.18.234.93"
    })


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    msg = data.get('message', '')
    if not msg:
        return jsonify({'error': 'message field required'}), 400

    cleaned = clean_text(msg)
    toks = tokenize_and_lemmatize(cleaned)
    joined = ' '.join(toks)

    seq = texts_to_padded_sequences(tokenizer, [joined], maxlen=100)
    tfidf_vec = tfidf.transform([joined]).toarray()

    prob = float(model.predict([seq, tfidf_vec])[0][0])
    pred_label = 'Spam' if prob >= 0.5 else 'Not Spam'
    confidence = f"{prob*100:.1f}%" if prob >= 0.5 else f"{(1-prob)*100:.1f}%"

    if prob >= 0.85:
        risk = 'High'
    elif prob >= 0.6:
        risk = 'Medium'
    else:
        risk = 'Low'

    keywords = extract_keywords(msg)

    return jsonify({
        'prediction': pred_label,
        'confidence': confidence,
        'risk_level': risk,
        'keywords': keywords
    })


if __name__ == '__main__':
    load_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=True)
