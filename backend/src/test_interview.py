import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Use the correct model
BASE_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

# Demonstrate interview capability with system instruction
payload = {
    "contents": [{
        "parts": [{"text": "I have 5 years of experience in Python development."}]
    }],
    "systemInstruction": {
        "parts": [{
            "text": """You are an AI interviewer conducting a Technical Interview.
Your role is to:
1. Ask ONE follow-up question based on the candidate's answer
2. Keep responses SHORT (1-2 sentences max)
3. Be professional and encouraging
4. Dig deeper into technical details

The candidate just answered a question. Now ask a relevant follow-up question about their Python experience."""
        }]
    },
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 100
    }
}

try:
    print("🔄 Testing Gemini Interview AI...\n")
    print("📝 Candidate says: 'I have 5 years of experience in Python development.'\n")
    
    response = requests.post(f"{BASE_URL}?key={API_KEY}", json=payload, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    ai_response = result['candidates'][0]['content']['parts'][0]['text']
    
    print("✅ SUCCESS! Gemini is working as an AI Interviewer!\n")
    print(f"🎤 AI Interviewer asks:\n{ai_response}\n")
    print("=" * 60)
    print("✅ The AI is READY for interviews!")
    print("✅ NO custom training needed - Gemini already understands")
    print("   interview context through system prompts!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
