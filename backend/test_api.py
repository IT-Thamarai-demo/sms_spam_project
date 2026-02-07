import requests
import time
import subprocess
import sys
import os

def test_api():
    print("Starting Flask server for testing...")
    # Start server as a background process
    # Use the current python executable
    server_process = subprocess.Popen([sys.executable, "backend/app.py"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT,
                                    text=True)
    
    # Wait for server to start
    time.sleep(5)
    
    url = "http://127.0.0.1:5000/predict"
    
    test_messages = [
        {
            "name": "High Risk Phishing",
            "message": "URGENT: Your account is suspended. Click here to verify: http://bit.ly/secure-login-bank",
        },
        {
            "name": "Medium Risk Spam",
            "message": "Congratulations! You won a free prize. Call 0800123456 now to claim.",
        },
        {
            "name": "Low Risk Ham",
            "message": "Hey, are we still meeting for lunch at 1pm? Let me know.",
        }
    ]
    
    try:
        for test in test_messages:
            print(f"\nTesting: {test['name']}")
            print(f"Message: {test['message']}")
            response = requests.post(url, json={"message": test['message']})
            if response.status_code == 200:
                print("Response:", response.json())
            else:
                print(f"API Error: {response.status_code}", response.text)
    
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        print("\nShutting down server...")
        server_process.terminate()

if __name__ == "__main__":
    # Ensure current dir is root
    test_api()
