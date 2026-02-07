# 30 External Viva Questions & Answers

### 1. What is the title of your project?
**Answer**: Face SMS Filtering System Using Hybrid CNN–BiLSTM.

### 2. Why did you choose a "Hybrid" model?
**Answer**: CNN is excellent for local feature extraction (finding keywords), while BiLSTM is great for understanding long-term dependencies and context in text. Combining them gives better performance than using them individually.

### 3. What is the difference between RNN and BiLSTM?
**Answer**: RNNs suffer from vanishing gradient problems. LSTM solves this with gates. BiLSTM processes data in both forward and backward directions, capturing more context.

### 4. What dataset did you use for training?
**Answer**: We used a combined dataset of traditional SMS Spam collection and modern Smishing datasets to ensure the model detects latest threats.

### 5. What is "Smishing"?
**Answer**: Smishing is "SMS Phishing," where attackers send deceptive messages to steal sensitive information like passwords or bank details.

### 6. Why did you use Flask for the backend?
**Answer**: Flask is a lightweight WSGI web application framework. It is perfect for hosting Python-based deep learning models as APIs.

### 7. How does the Android app communicate with the server?
**Answer**: We use the Retrofit library to make HTTP POST requests to the Flask server and receive JSON responses.

### 8. Where is the scan history stored?
**Answer**: It is stored locally on the Android device using an SQLite database.

### 9. What is the role of CNN in your model?
**Answer**: CNN acts as a feature extractor. It uses filters to find sequences of words that are common in spam messages.

### 10. What is "Tokenization" in NLP?
**Answer**: It is the process of breaking down a sentence into individual words or "tokens" so the model can process them.

### 11. What is "Padding" in your model?
**Answer**: Since different SMS have different lengths, we use padding (adding zeros) to make all input sequences the same length for the neural network.

### 12. What is "Word Embedding"?
**Answer**: It is a way of representing words as numerical vectors where similar words have similar vector values. We used a layer to learn these embeddings.

### 13. What is "Accuracy" vs "Precision"?
**Answer**: Accuracy is the overall correctness. Precision is how many of the predicted "Spam" messages were actually "Spam." In spam detection, high precision is important to avoid marking safe messages as spam.

### 14. How do you handle "Stopwords"?
**Answer**: Stopwords (like 'is', 'the', 'at') are common words that don't add much meaning. We remove them during preprocessing to reduce noise.

### 15. What are the activation functions used?
**Answer**: We typically use ReLU for internal layers and Sigmoid/Softmax for the final output layer to get probabilities.

### 16. What is the "Confidence Score"?
**Answer**: It is the probability (0 to 1 converted to %) returned by the model output (Sigmoid function).

### 17. How can you deploy this in real-time?
**Answer**: Currently, it runs on localhost. For real-world use, we can deploy the Flask server on AWS, Google Cloud, or Heroku.

### 18. What is the "Risk Level" based on?
**Answer**: It is based on the confidence score. For example, >90% is High Risk, 60-90% is Medium, and <60% is Low.

### 19. Why use SQLite instead of Firebase?
**Answer**: For this project scope, local SQLite is faster for history tracking and doesn't require an internet connection to view previous results.

### 20. What is the purpose of the Splash Screen?
**Answer**: To provide a professional branding experience and allow the app to initialize configurations in the background.

### 21. What library is used for JSON parsing in Android?
**Answer**: GSON (Google GSON).

### 22. What is the advantage of using Material Design 3?
**Answer**: It provides a modern, adaptive, and premium look-and-feel that follows Google's latest design standards.

### 23. How do you handle Internet permissions in Android?
**Answer**: By adding `<uses-permission android:name="android.permission.INTERNET" />` in the `AndroidManifest.xml` file.

### 24. What is "Dropout" in neural networks?
**Answer**: It is a regularisation technique where some neurons are randomly "dropped" during training to prevent overfitting.

### 25. What is "Overfitting"?
**Answer**: It's when the model performs very well on training data but poorly on new, unseen data.

### 26. How did you create the APK?
**Answer**: Using the Build -> Build APK(s) option in Android Studio.

### 27. What is the "Namespace" in Android `build.gradle`?
**Answer**: It is the unique package identifier for the application (e.g., `com.example.smspam`).

### 28. What is a "RecyclerView"?
**Answer**: It is an advanced version of ListView that efficiently displays large sets of data by recycling views that have scrolled off-screen.

### 29. Can your model detect image-based spam (MMS)?
**Answer**: No, current scope only covers text-based SMS. For MMS, we would need OCR (Optical Character Recognition).

### 30. What is your future scope for this project?
**Answer**: We can add SMS auto-blocking features, support for multiple languages, and real-time notification interception.
