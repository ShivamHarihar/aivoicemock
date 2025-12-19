import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# List available models
url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

try:
    print("🔄 Fetching available Gemini models...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    models = result.get('models', [])
    
    print(f"\n✅ Found {len(models)} available models:\n")
    for model in models:
        name = model.get('name', 'Unknown')
        display_name = model.get('displayName', 'Unknown')
        supported_methods = model.get('supportedGenerationMethods', [])
        
        if 'generateContent' in supported_methods:
            print(f"✓ {name}")
            print(f"  Display Name: {display_name}")
            print(f"  Methods: {', '.join(supported_methods)}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
