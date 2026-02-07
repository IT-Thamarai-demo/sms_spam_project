import os

# Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = PROJECT_ROOT  # Datasets are expected in the project root

# Dataset Config
DATASET_1_NAME = "Dataset_10191.csv"
DATASET_2_NAME = "spam.csv"
UCI_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"

# Model Config
MAX_WORDS = 10000
MAX_LEN = 100
EMBEDDING_DIM = 300
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Paths for saving artifacts
MODEL_PATH = os.path.join(BASE_DIR, "sms_model.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl")
