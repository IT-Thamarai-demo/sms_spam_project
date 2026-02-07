import sys
import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Add backend directory to path
sys.path.append(r'c:\Users\Asus\Desktop\smstrain\sms_spam_project\backend')

from config import *
from preprocessing import preprocess_text

def get_keywords(text, tfidf_vectorizer):
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

def test_full_pipeline():
    print("Testing full pipeline for 'hoi'...")
    try:
        # Preprocess
        clean = preprocess_text("hoi")
        print(f"Clean text: '{clean}'")
        
        # Load artifacts
        print("Loading artifacts...")
        model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer = pickle.load(f)
        with open(TFIDF_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
            
        # 1. Predict
        seq = tokenizer.texts_to_sequences([clean])
        padded = pad_sequences(seq, maxlen=MAX_LEN)
        prob = float(model.predict(padded)[0][0])
        print(f"Prediction probability: {prob}")
        
        # 2. Keywords
        keywords = get_keywords(clean, tfidf_vectorizer)
        print(f"Keywords: {keywords}")
        
        print("SUCCESS!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline()
