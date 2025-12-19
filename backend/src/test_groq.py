import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")  # Actually Groq key
print(f"API Key: {API_KEY[:20]}...")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are an AI interviewer. Ask ONE technical interview question about Python. Keep it to 1-2 sentences."},
        {"role": "user", "content": "I have 5 years of Python experience."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    print("\n🔄 Testing Groq API...")
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    ai_response = result['choices'][0]['message']['content']
    
    print("✅ SUCCESS! Groq is working!\n")
    print(f"🎤 AI Interviewer:\n{ai_response}\n")
    print("=" * 60)
    print("✅ Groq is FASTER than Gemini!")
    print("✅ Perfect for real-time interviews!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
