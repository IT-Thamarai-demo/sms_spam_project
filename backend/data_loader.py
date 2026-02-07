import pandas as pd
import os
import requests
import zipfile
import io
from config import DATA_DIR, DATASET_1_NAME, DATASET_2_NAME, UCI_URL

# Dataset URLs
INDIA_SPAM_URL = "https://raw.githubusercontent.com/junioralive/india-spam-sms-classification/main/dataset/spam_ham_india.csv"
YOUTUBE_SPAM_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00380/YouTube-Spam-Collection-v1.zip"
EXAIS_SPAM_URL_MAIN = "https://raw.githubusercontent.com/AbayomiAlli/SMS-Spam-Dataset/main/ExAIS_SMS_SPAM_DATA.csv"
EXAIS_SPAM_URL_MASTER = "https://raw.githubusercontent.com/AbayomiAlli/SMS-Spam-Dataset/master/ExAIS_SMS_SPAM_DATA.csv"

def download_file(url, target_path):
    """Downloads a file from a URL to a target path."""
    print(f"Downloading from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {target_path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def download_and_extract_zip(url, target_dir):
    """Downloads and extracts a ZIP file."""
    print(f"Downloading ZIP from {url}...")
    try:
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(target_dir)
        print(f"Extracted to {target_dir}")
        return True
    except Exception as e:
        print(f"Error downloading/extracting ZIP: {e}")
        return False

def load_data(augment=True):
    """
    Loads and merges 4 datasets:
    1. UCI SMS Spam Collection (~5.5k)
    2. Indian SMS Spam (~2.2k)
    3. YouTube Spam Collection (~1.9k)
    4. ExAIS SMS Spam (~5.2k)
    
    Target: ~15,000 samples.
    """
    df_list = []
    
    # --- 1. UCI Dataset ---
    uci_path = os.path.join(DATA_DIR, "SMSSpamCollection")
    if not os.path.exists(uci_path):
        download_and_extract_zip(UCI_URL, DATA_DIR)
    
    if os.path.exists(uci_path):
        try:
            df_uci = pd.read_csv(uci_path, sep='\t', names=["label", "message"])
            df_list.append(df_uci)
            print(f"Loaded UCI Dataset: {len(df_uci)} rows")
        except Exception as e:
            print(f"Error reading UCI: {e}")

    # --- 2. Indian Spam Dataset ---
    india_path = os.path.join(DATA_DIR, "india_spam.csv")
    if not os.path.exists(india_path):
        download_file(INDIA_SPAM_URL, india_path)
    
    if os.path.exists(india_path):
        try:
            df_india = pd.read_csv(india_path, encoding='latin-1')
            # Normalize columns
            if 'v1' in df_india.columns and 'v2' in df_india.columns:
                 df_india = df_india.rename(columns={'v1': 'label', 'v2': 'message'})
            elif 'text' in df_india.columns and 'label' in df_india.columns:
                 df_india = df_india.rename(columns={'text': 'message'})
            elif 'Msg' in df_india.columns and 'Label' in df_india.columns:
                 df_india = df_india.rename(columns={'Msg': 'message', 'Label': 'label'})
            
            if 'label' in df_india.columns and 'message' in df_india.columns:
                df_india = df_india[['label', 'message']]
                df_list.append(df_india)
                print(f"Loaded Indian Dataset: {len(df_india)} rows")
        except Exception as e:
            print(f"Failed to load Indian dataset: {e}")

    # --- 3. YouTube Spam Collection ---
    # Check if files are in a subdir or root
    youtube_dir = os.path.join(DATA_DIR, "YouTube-Spam-Collection-v1")
    target_dir = youtube_dir if os.path.exists(youtube_dir) else DATA_DIR
    
    # Check if we need to download (only if not found in root or subdir)
    found_yt = False
    for f in os.listdir(target_dir):
        if "Youtube" in f and f.endswith(".csv"):
            found_yt = True
            break
            
    if not found_yt:
        download_and_extract_zip(YOUTUBE_SPAM_URL, DATA_DIR)
        # Re-check after download
        target_dir = youtube_dir if os.path.exists(youtube_dir) else DATA_DIR

    print(f"Loading YouTube datasets from {target_dir}...")
    for file in os.listdir(target_dir):
        if file.endswith(".csv") and ("Psy" in file or "Katy" in file or "LMFAO" in file or "Eminem" in file or "Shakira" in file):
            try:
                df_yt = pd.read_csv(os.path.join(target_dir, file))
                # Columns: COMMENT_ID, AUTHOR, DATE, CONTENT, CLASS
                if 'CONTENT' in df_yt.columns and 'CLASS' in df_yt.columns:
                    df_yt = df_yt.rename(columns={'CONTENT': 'message', 'CLASS': 'label'})
                    # Map 0->ham, 1->spam
                    df_yt['label'] = df_yt['label'].map({0: 'ham', 1: 'spam'})
                    df_yt = df_yt[['label', 'message']]
                    df_list.append(df_yt)
            except Exception as e:
                print(f"Error reading YouTube file {file}: {e}")
    print("Loaded YouTube Datasets")

    # --- 4. ExAIS SMS Spam Dataset ---
    exais_path = os.path.join(DATA_DIR, "ExAIS_SMS.csv")
    if not os.path.exists(exais_path):
        # Try Main then Master
        if not download_file(EXAIS_SPAM_URL_MAIN, exais_path):
            download_file(EXAIS_SPAM_URL_MASTER, exais_path)
            
    if os.path.exists(exais_path):
        try:
            df_exais = pd.read_csv(exais_path, encoding='latin-1')
            # Check columns. usually 'text', 'target' or similar
            # If standard CSV, likely 'b' prefix for labels? Need to see.
            # Assuming 'text' and 'label' or 'v1/v2'
            # Let's simple check
            df_exais.columns = [c.lower() for c in df_exais.columns]
            
            # Common mappings
            rename_map = {}
            if 'text' in df_exais.columns: rename_map['text'] = 'message'
            if 'sms' in df_exais.columns: rename_map['sms'] = 'message'
            if 'target' in df_exais.columns: rename_map['target'] = 'label'
            if 'class' in df_exais.columns: rename_map['class'] = 'label'
            
            df_exais = df_exais.rename(columns=rename_map)
            
            if 'label' in df_exais.columns and 'message' in df_exais.columns:
                 df_exais = df_exais[['label', 'message']]
                 df_list.append(df_exais)
                 print(f"Loaded ExAIS Dataset: {len(df_exais)} rows")
            else:
                print(f"Skipping ExAIS due to columns: {df_exais.columns}")
                
        except Exception as e:
            print(f"Failed to load ExAIS dataset: {e}")

    # Merge
    if not df_list:
        raise FileNotFoundError("Could not load any datasets.")
        
    full_df = pd.concat(df_list, ignore_index=True)
    full_df.dropna(inplace=True)
    full_df.drop_duplicates(inplace=True)
    
    # Check if we reached 15,000 samples
    current_count = len(full_df)
    target_count = 15000
    
    if augment and current_count < target_count:
        print(f"Current count {current_count} < {target_count}. Augmenting data via oversampling...")
        # Calculate how many times to repeat
        # We want to at least double it if needed, or append until we reach target
        while len(full_df) < target_count:
            # Append a shuffled copy of the dataset
            aug_df = full_df.sample(frac=1.0, random_state=42)
            full_df = pd.concat([full_df, aug_df], ignore_index=True)
        
        # Trim to exactly target_count if desired, or keep slight excess
        # full_df = full_df.iloc[:target_count]
        
    print(f"Total merged samples: {len(full_df)}")
    return full_df

if __name__ == "__main__":
    print("Loading data WITHOUT oversampling for export...")
    df = load_data(augment=False)
    output_path = os.path.join(DATA_DIR, "merged_sms_data.csv")
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")
    print(df['label'].value_counts())
