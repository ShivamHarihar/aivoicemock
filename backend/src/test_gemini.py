import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {API_KEY[:20]}..." if API_KEY and len(API_KEY) > 20 else f"API Key: {API_KEY}")

if not API_KEY or API_KEY == "your_gemini_api_key_here":
    print("❌ ERROR: API key is missing or is still the placeholder!")
    exit(1)

# Test API call with v1 endpoint
BASE_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

# Test with interview-specific prompt
interview_prompt = """You are an AI interviewer conducting an HR interview.
Ask me ONE interview question about my experience with teamwork.
Keep your response to 1-2 sentences only."""

payload = {
    "contents": [{
        "parts": [{"text": interview_prompt}]
    }]
}

try:
    print("\n🔄 Testing Gemini API connection...")
    response = requests.post(f"{BASE_URL}?key={API_KEY}", json=payload, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    ai_response = result['candidates'][0]['content']['parts'][0]['text']
    
    print("✅ SUCCESS! Gemini API is working!")
    print(f"\n🎤 AI Interviewer says:\n{ai_response}")
    print("\n✅ The AI is ready to conduct interviews!")
    
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    print(f"Response: {e.response.text if hasattr(e, 'response') else 'No response'}")
except Exception as e:
    print(f"❌ Error: {e}")
