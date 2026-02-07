# Face SMS Filtering System Using Hybrid CNN–BiLSTM

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/IT-Thamarai-demo/sms_spam_project)

This project implements a state-of-the-art SMS spam and phishing detection system. It features a Hybrid CNN-BiLSTM model trained on a massive dataset of ~78k unique samples.

## 🚀 Key Features (Proposed System)
1.  **Multimodal Detection**: Analyzes both SMS text and embedded URLs.
2.  **Explainable AI (XAI)**: Highlights the specific keywords (e.g., 'urgent', 'verify', 'congratulations') that triggered the classification.
3.  **Risk Scoring System**: Categorizes messages into **High**, **Medium**, or **Low** risk based on probability scores.
4.  **Massive Dataset**: Trained on 78,838 unique samples (UCI + India + YouTube + Smishing datasets).

## 📂 Project Structure
- `backend/`: Python Flask API, Model Training, and Preprocessing.
- `android_app/`: Native Java Android application source code.
- `proposed_dataset.csv`: The comprehensive training dataset.

## 🛠️ How to Run

### Backend
1.  Install requirements: `pip install -r requirements.txt`
2.  Train (Optional): `python backend/train.py` (Artifacts already provided)
3.  Start Server: `python backend/app.py`

### Android
1.  Open the `android_app` folder in Android Studio.
2.  Run on an emulator or physical device.
    - Note: The app connects to `10.0.2.2:5000` (localhost for emulator).

## 📊 Model Performance
- **Accuracy**: 97%
- **F1-Score**: 0.97
- Tested against phishing links, promotional spam, and legitimate personal messages.
