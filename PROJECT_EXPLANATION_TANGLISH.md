# Proposed System Explanation (Tanglish)

Intha folder la namma project oda current implementation pathi clear ah explain pannirukkom.

## 1. What is the Problem?
Normal ah SMS spam detect panna simple patterns use pannuvanga. Aana ippo ellam "Smishing" (SMS + Phishing) romba advance aaiduchi. Simple rules vechi ithai kandupudika mudiyathu. So, namma oru **Deep Learning** based system propose pannirukkom.

## 2. Proposed System: Hybrid CNN-BiLSTM
Namma project la rendu powerful algorithms ah mix pannirukkom:
- **CNN (Convolutional Neural Network)**: SMS la irukara important words and patterns ah fast ah identify pannum.
- **BiLSTM (Bidirectional Long Short-Term Memory)**: SMS oda context (munnadi pinnadi irukira words oda relation) ah purinjukum.

Intha rendum combine aagi varapo, accuracy romba athigama irukum.

## 3. How it Works? (Flow)
1. **Input**: User Android app la scan panna vendiya SMS ah paste pannuvanga.
2. **Backend**: App intha message ah namma Flask Server ku anupum.
3. **Preprocessing**: Server la message clean panna padum (stopwords removal, tokenization).
4. **Prediction**: Deep Learning model intha message "Spam" ah illa "Safe" ah nu predict pannum.
5. **Output**: Result (Spam/Not Spam), Confidence score, and Risk level app la display aagum.

## 4. Key Features
- **Modern UI**: Clean design for easy usage.
- **Clipboard Integration**: Fast ah message paste pannalam.
- **Local History**: Scanned messages list ah eppo venum nalum check pannalam (Stored in SQLite).
- **Real-time Detection**: Flask backend vechi instant ah result kidaikum.

Intha system final year project ku perfect ah suitable aagum, because ithula deep learning concept and full-stack android development mix aagi iruku.
