# PROJECT DOCUMENTATION: MODULE DESCRIPTIONS AND MODULE DESIGN

**Project Title:** Face SMS Filtering System Using Hybrid CNN–BiLSTM
**Project Domain:** Artificial Intelligence / Android Development / Deep Learning

---

## 1. MODULE DESCRIPTIONS

The proposed system is divided into five primary modules that work together to provide real-time SMS classification and security. Each module is designed to handle a specific stage of the data lifecycle, from user interaction to deep learning prediction.

### Module 1: User Interface and Interactive Layer (Android Client)
This module serves as the primary gateway for user interaction. It is developed using Material Design 3 guidelines to provide a professional and intuitive user experience.
- **Purpose**: To provide a platform for users to input SMS text, view classification results, and navigate through the application’s features.
- **Input**: Raw alphanumeric SMS text entered manually or pasted via the clipboard.
- **Process**: Captures the user’s input, validates the text length, maintains the UI state during active scans, and triggers the communication module.
- **Output**: Visual results including the prediction category (Spam/Not Spam), confidence score, risk level, and a list of detected keywords.

### Module 2: API Gateway and Communication Interface (Retrofit Client)
This module acts as the bridge between the mobile application and the remote deep learning backend server.
- **Purpose**: To facilitate secure and asynchronous data exchange between the client and the server.
- **Input**: Encapsulated JSON request objects containing the SMS message payload.
- **Process**: Serializes Java objects into JSON format, establishes an HTTP connection to the Flask server, and manages background network threads to prevent UI freezing.
- **Output**: Deserialized response objects containing the model’s prediction and metadata.

### Module 3: Data Pre-processing and Transformation Module (NLP Engine)
Located on the backend server, this module prepares raw text for analysis by the neural network.
- **Purpose**: To clean and transform unstructured text into a numerical format that the deep learning model can interpret.
- **Input**: Raw text payload received from the API gateway.
- **Process**: Performs Natural Language Processing (NLP) tasks including tokenization, removal of stop words, special character filtering, and numerical vectorization using pre-trained vocabulary dictionaries.
- **Output**: Padded numerical sequences ready for the classification engine.

### Module 4: Hybrid Feature Extraction and Classification Module (CNN-BiLSTM Model)
The core intelligence of the system, this module utilizes a hybrid architecture combining Convolutional Neural Networks (CNN) and Bidirectional Long Short-Term Memory (BiLSTM).
- **Purpose**: To analyze patterns and contextual relationships within the text to determine the intent of the message.
- **Input**: Pre-processed numerical sequences (tensors).
- **Process**: The CNN layers extract local spatial features (keywords), while the BiLSTM layers capture long-range contextual dependencies from both directions (forward and backward). A final dense layer calculates the probability of the message being spam.
- **Output**: Probability scores and categorical prediction labels.

### Module 5: Persistent Data Management Module (SQLite Storage)
This module handles local data retention on the user’s device for auditing and historical review.
- **Purpose**: To maintain a record of all previous scans so users can track identified threats over time.
- **Input**: Successful scan results and timestamps from the interactive layer.
- **Process**: Inserts scan records into the local SQLite database and executes optimized queries to retrieve history for the RecyclerView display.
- **Output**: Historical lists of messages with their relative risk levels and prediction outcomes.

---

## 2. MODULE DESIGN

The project follows a **Client-Server Architectural Style** with a clear separation of concerns between the mobile frontend and the intelligence backend. The design is structured to ensure scalability, low latency, and ease of maintenance.

### System Interaction and Integration
The system initiates when the User Interface Module captures an SMS message. This data is passed to the Communication Interface, which establishes a connection with the Backend Server. Once the server accepts the request, the Pre-processing Module cleans the data and passes it to the Hybrid Model. The resulting prediction is sent back through the API Gateway to the Android Client, which simultaneously displays the result to the user and commits the record to the Persistent Data Management Module.

### Data Flow Architecture
The data flow within the system is unidirectional and follows a strictly defined path:
1. **Request Flow**: Raw Text (Android App) → JSON Payload (API Gateway) → Pre-processed Vectors (NLP Engine) → Feature Maps (CNN-BiLSTM).
2. **Response Flow**: Probability Scores (Model) → Prediction Metadata (API Gateway) → Result Cards & SQLite (Android Client).

### Selection of Architecture
A **Layered Architecture** approach is adopted within both the client and server. The client utilizes a view-based separation to isolate UI logic from database operations. The server maintains a modular distinction between the API routing layer and the deep learning inference layer. This design ensures that the model can be updated or retrained without requiring modifications to the mobile application's source code, making the system future-proof and production-ready.
