# Setup Guide - SMS Spam Detector (Hybrid CNN-BiLSTM)

This project is an AI-powered SMS Spam Detection system featuring a modern Android application and a Flask-based deep learning backend.

## Architecture
- **Android App**: User interface for scanning SMS and viewing history.
- **Backend (Flask)**: Hosts the CNN-BiLSTM model for real-time predictions.
- **Model**: Hybrid CNN-BiLSTM trained on a massive smishing dataset.

## Prerequisite
1. **Python 3.8+**
2. **Android Studio** (for building/deploying the app)
3. **Android Emulator/Device**

## Backend Setup
1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
   *The server runs on `http://localhost:5000`.*

## Android App Setup
1. Open the `android_app` folder in Android Studio.
2. Wait for Gradle sync to complete.
3. If running on a physical device, update `RetrofitClient.java` with your computer's IP address.
4. Build and run the application.

## Project Structure
- `android_app/`: Complete Android Studio project.
- `backend/`: Flask server, model files, and preprocessing logic.
- `docs/media/`: Demo screenshots and video.
