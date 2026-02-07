# MODULE DESCRIPTIONS

The proposed Face SMS Filtering System Using Hybrid CNN–BiLSTM is divided into the following functional modules to ensure modularity, scalability, and ease of maintenance.

### 1. Dataset Collection Module
This module is responsible for collecting SMS datasets from multiple sources. It first checks for locally available datasets such as `Dataset_10191.csv` and `spam.csv`. If they are not found, the system automatically downloads publicly available SMS spam datasets from online repositories. All datasets are merged, cleaned, and duplicates are removed to form a unified dataset.

### 2. Text Preprocessing Module
This module prepares raw SMS messages for model training and prediction. It performs operations such as converting text to lowercase, removing punctuation and numbers, tokenization, stopword removal, and lemmatization. This ensures that the input text is clean and consistent for feature extraction.

### 3. Feature Extraction Module
In this module, meaningful numerical features are extracted from the preprocessed text. TF-IDF vectorization is used to capture word importance, while Word2Vec embeddings (300 dimensions) are used to capture semantic relationships between words. These features serve as input to the deep learning model.

### 4. Hybrid CNN–BiLSTM Model Module
This module implements the core spam detection logic. A hybrid deep learning model combining CNN and Bidirectional LSTM is used. CNN captures local textual patterns, while BiLSTM captures long-term contextual dependencies. The model outputs a probability indicating whether an SMS is spam or not.

### 5. Flask Backend API Module
This module exposes the trained model as a REST API using Flask. It receives SMS messages from the Android application, performs preprocessing and prediction, and returns results such as spam status, confidence level, risk level, and detected keywords.

### 6. Android Application Module
This module provides the user interface. Users can enter or paste SMS messages and scan them for spam. The app communicates with the backend using Retrofit and displays results using a clean Material Design UI. A history module stores scanned messages locally using SQLite.

---

# MODULE DESIGN

The system follows a modular and layered architecture, ensuring clear separation between data processing, model computation, backend services, and user interface.

### 1. Dataset & Preprocessing Design
The dataset module feeds SMS data into the preprocessing pipeline. Preprocessing functions are designed as reusable components to ensure consistency during both training and real-time prediction.

### 2. Feature Engineering Design
TF-IDF and Word2Vec features are generated in parallel and combined to provide both statistical and semantic representations of SMS text. These features are standardized before being passed to the model.

### 3. Model Design
The hybrid CNN–BiLSTM model is designed to improve classification accuracy. CNN layers extract local n-gram features, while BiLSTM layers analyze bidirectional contextual dependencies. Dropout layers are added to reduce overfitting, and a sigmoid output layer performs binary classification.

### 4. Backend Design
The Flask backend is designed using REST principles. It loads the trained model and preprocessing artifacts once during startup to reduce latency. The `/predict` endpoint handles prediction requests efficiently and returns structured JSON responses.

### 5. Android UI Design
The Android application follows Material Design guidelines. Screens are designed to be simple and intuitive, with color-based feedback (red for spam, green for safe messages). SQLite is used for local storage of scan history to support offline access.

### 6. Overall System Flow
User input → Android UI → Flask API → Preprocessing → Feature Extraction → CNN–BiLSTM Model → Prediction → Result displayed in Android UI.
