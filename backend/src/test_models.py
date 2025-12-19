import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Try gemini-1.5-flash
models_to_try = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro"
]

for model_name in models_to_try:
    BASE_URL = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Say 'Hello, I am working!' in one sentence."}]
        }]
    }
    
    try:
        print(f"\n🔄 Testing {model_name}...")
        response = requests.post(f"{BASE_URL}?key={API_KEY}", json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['candidates'][0]['content']['parts'][0]['text']
        
        print(f"✅ SUCCESS with {model_name}!")
        print(f"Response: {ai_response}")
        print(f"\n✅ Use this model: {model_name}")
        break
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed with {model_name}: {e.response.status_code}")
        continue
    except Exception as e:
        print(f"❌ Error with {model_name}: {e}")
        continue
else:
    print("\n❌ None of the models worked. Your API key might have restrictions.")
    print("Try creating a new API key at: https://aistudio.google.com/app/apikey")
