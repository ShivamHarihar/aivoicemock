import os
import logging
import json
import requests
from .prompts import SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)

# Configure Groq API
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

if not API_KEY:
    logger.warning("GROQ_API_KEY not found in environment variables.")
else:
    logger.info("GROQ API Key loaded successfully")


def generate_response(prompt):
    """Generates a response from Grok using REST API."""
    if not API_KEY:
        return {"reaction": "Error", "follow_up_question": "API Key missing.", "score": 0, "feedback": "Config Error"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Parse Grok response
        try:
            text_content = result['choices'][0]['message']['content']
            return json.loads(text_content)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse Grok response: {e}. Raw: {result}")
            return {"reaction": "I see.", "follow_up_question": "Could you elaborate?", "score": 5, "feedback": "Parse Error"}
            
    except Exception as e:
        logger.error(f"Grok API Error: {e}")
        return {"reaction": "Hmm...", "follow_up_question": "Let's continue.", "score": 0, "feedback": "API Error"}

def generate_text_response(prompt):
    """Generates a plain text response (non-JSON)."""
    if not API_KEY:
        return "API Key missing."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
            
    except Exception as e:
        logger.error(f"Grok Text API Error: {e}")
        return "I apologize, I'm having trouble connecting."

def generate_resume_analysis(prompt):
    """Generates a resume analysis response from Grok."""
    if not API_KEY:
        return {"error": "API Key missing."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    try:
        logger.info("Using Groq for resume analysis...")
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Parse Groq response
        try:
            text_content = result['choices'][0]['message']['content']
            return json.loads(text_content)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse Groq resume analysis: {e}. Raw: {result}")
            return {"error": "Failed to parse AI response"}
            
    except requests.exceptions.HTTPError as e:
        logger.error(f"Grok API HTTP Error: {e}")
        logger.error(f"Response status: {e.response.status_code}")
        logger.error(f"Response body: {e.response.text}")
        
        # Handle rate limits gracefully
        if "rate_limit" in str(e.response.text).lower():
            return {
                "error": "API rate limit reached",
                "message": "Groq API rate limit reached. Please wait a few minutes and try again, or check back later.",
                "overall_score": 70,  # Default score so UI doesn't break
                "summary": "Analysis temporarily unavailable due to API limits.",
                "factor_scores": {"impact": 70, "skills": 70, "formatting": 70, "brevity": 70},
                "strengths": ["Unable to analyze at this time"],
                "weaknesses": ["Please try again in a few minutes"],
                "career_roadmap": ["Wait for API limits to reset"]
            }
        
        return {"error": f"Grok API error: {e.response.text}"}
    except Exception as e:
        logger.error(f"Grok Resume Analysis API Error: {e}")
        return {"error": str(e)}
