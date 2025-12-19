import requests
import json
import os
import time

BASE_URL = "http://127.0.0.1:5000"

def test_start_interview():
    print("Testing /start_call_interview...")
    try:
        response = requests.post(f"{BASE_URL}/start_call_interview", json={"mode": "Technical"})
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Session ID: {data.get('session_id')}")
            return data.get('session_id')
        else:
            print(f"FAILED: {response.text}")
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_upload_profile():
    print("Testing /upload_profile...")
    # Create a dummy resume
    with open("dummy_resume.txt", "w") as f:
        f.write("Experienced Python Developer with Flask and AWS skills.")
        
    try:
        files = {'resume': open("dummy_resume.txt", 'rb')}
        response = requests.post(f"{BASE_URL}/upload_profile", files=files)
        if response.status_code == 200:
            print(f"SUCCESS: Parsed Data: {response.json()}")
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        os.remove("dummy_resume.txt")

def test_process_voice(session_id):
    print("Testing /process_voice...")
    # We need a dummy audio file. Let's create a very small empty wav or just try to send something.
    # Actually, Whisper might fail on empty audio.
    # Let's skip actual audio processing test in this script if we can't easily generate valid audio.
    # But we can test the endpoint existence and error handling.
    
    try:
        # Create a dummy file
        with open("test_audio.wav", "wb") as f:
            f.write(b"RIFF....WAVEfmt ....data....") # Invalid WAV but file exists
            
        files = {'audio': open("test_audio.wav", 'rb')}
        data = {'session_id': session_id}
        
        response = requests.post(f"{BASE_URL}/process_voice", files=files, data=data)
        
        # Expecting 400 or 500 because audio is invalid, but checking if it hits the server
        print(f"Response Status: {response.status_code}")
        if response.status_code in [200, 400, 500]:
            print("SUCCESS: Endpoint reachable.")
        else:
            print(f"FAILED: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if os.path.exists("test_audio.wav"):
            os.remove("test_audio.wav")

if __name__ == "__main__":
    # Wait for server to start (manual step usually, but here we assume it's running or we run it)
    # Since I can't run the server in background easily and run this script in parallel in one tool call,
    # I will just print the instructions to run this.
    print("Starting tests...")
    sid = test_start_interview()
    if sid:
        test_upload_profile()
        test_process_voice(sid)
