import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Embedding, Conv1D, Dropout
from config import MAX_WORDS, MAX_LEN, EMBEDDING_DIM

def build_hybrid_model(vocab_size, embedding_matrix=None):
    model = Sequential()
    
    # 1. Embedding
    if embedding_matrix is not None:
        model.add(Embedding(input_dim=vocab_size, 
                            output_dim=EMBEDDING_DIM, 
                            weights=[embedding_matrix], 
                            input_length=MAX_LEN, 
                            trainable=True))
    else:
        model.add(Embedding(input_dim=vocab_size, 
                            output_dim=EMBEDDING_DIM, 
                            input_length=MAX_LEN))

    # 2. CNN Block
    model.add(Conv1D(filters=128, kernel_size=5, activation='relu', padding='same'))
    model.add(tf.keras.layers.MaxPooling1D(pool_size=2))
    
    # 3. BiLSTM Block
    model.add(Bidirectional(LSTM(64, return_sequences=False))) 

    # 4. Dense Layers
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model
