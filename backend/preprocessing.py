import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4') # Open Multilingual Wordnet

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Applies the following steps:
    1. Lowercase
    2. Remove numbers and punctuation
    3. Tokenization
    4. Stopword removal
    5. Lemmatization
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove numbers and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 3. Tokenization
    tokens = nltk.word_tokenize(text)
    
    # 4 & 5. Stopword removal and Lemmatization
    clean_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    return " ".join(clean_tokens)

if __name__ == "__main__":
    sample = "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"
    print(f"Original: {sample}")
    print(f"Processed: {preprocess_text(sample)}")
