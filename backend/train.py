import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from sklearn.metrics import classification_report

from config import *
from data_loader import load_data
from preprocessing import preprocess_text
from model import build_hybrid_model

def train():
    print("Loading data...")
    # This will auto-download if missing
    df = load_data()
    
    print("Preprocessing text...")
    df['clean_text'] = df['message'].apply(preprocess_text)
    
    # X and y
    X_text = df['clean_text'].values
    y = df['label'].map({'ham': 0, 'spam': 1}).values
    
    # 1. TF-IDF Vectorization
    print("Fitting TF-IDF...")
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf.fit(X_text)
    with open(TFIDF_PATH, 'wb') as f:
        pickle.dump(tfidf, f)
    print("TF-IDF saved.")

    # 2. Word2Vec Embeddings
    print("Training Word2Vec...")
    sentences = [text.split() for text in X_text]
    w2v_model = Word2Vec(sentences, vector_size=EMBEDDING_DIM, window=5, min_count=1, workers=4)

    # 3. Keras Tokenizer
    print("Tokenizing for Deep Learning...")
    tokenizer = Tokenizer(num_words=MAX_WORDS)
    tokenizer.fit_on_texts(X_text)
    sequences = tokenizer.texts_to_sequences(X_text)
    X_pad = pad_sequences(sequences, maxlen=MAX_LEN)
    
    word_index = tokenizer.word_index
    vocab_size = min(MAX_WORDS, len(word_index) + 1)
    
    with open(TOKENIZER_PATH, 'wb') as f:
        pickle.dump(tokenizer, f)
    print("Tokenizer saved.")

    # 4. Create Embedding Matrix
    print("Creating Embedding Matrix...")
    embedding_matrix = np.zeros((vocab_size, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i >= MAX_WORDS:
            continue
        if word in w2v_model.wv:
            embedding_matrix[i] = w2v_model.wv[word]
        else:
            embedding_matrix[i] = np.random.normal(scale=0.6, size=(EMBEDDING_DIM,))
            
    # 5. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    
    # 6. Build and Train Model
    print("Building Model...")
    model = build_hybrid_model(vocab_size, embedding_matrix)
    model.summary()
    
    print("Training Model...")
    history = model.fit(X_train, y_train, 
                        epochs=5, 
                        batch_size=32, 
                        validation_data=(X_test, y_test))
    
    # 7. Evaluate
    print("Evaluating...")
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 8. Save Model
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
