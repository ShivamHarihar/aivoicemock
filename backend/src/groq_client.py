import os
import logging
import json
import requests
from .prompts import SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)

# Configure Groq
API_KEY = os.getenv("GEMINI_API_KEY")  # Using same env var for simplicity
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

if not API_KEY:
    logger.warning("GROQ API KEY not found in environment variables.")

def generate_response(prompt):
    """Generates a response from Groq using OpenAI-compatible API."""
    if not API_KEY:
        return {"reaction": "Error", "follow_up_question": "API Key missing.", "score": 0, "feedback": "Config Error"}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",  # Fast and good for conversations
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        
        # Parse response
        try:
            text_content = result['choices'][0]['message']['content']
            return json.loads(text_content)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse Groq response: {e}. Raw: {result}")
            return {"reaction": "I see.", "follow_up_question": "Could you elaborate?", "score": 5, "feedback": "Parse Error"}
            
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return {"reaction": "Hmm...", "follow_up_question": "Let's continue.", "score": 0, "feedback": "API Error"}

def generate_text_response(prompt):
    """Generates a plain text response (non-JSON)."""
    if not API_KEY:
        return "API Key missing."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
            
    except Exception as e:
        logger.error(f"Groq Text API Error: {e}")
        return "I apologize, I'm having trouble connecting."
