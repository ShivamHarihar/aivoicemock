"""
Enhanced Grok Client with Free AI Fallback
Automatically uses free AI providers when primary Groq key is exhausted
"""

import os
import logging
import json
import requests
import asyncio
from .prompts import SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)

# Primary Groq API configuration
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Free AI system flag
USE_FREE_AI = os.getenv("USE_FREE_AI", "true").lower() == "true"
free_ai_manager = None

if not API_KEY:
    logger.warning("GROQ_API_KEY not found in environment variables.")
    if USE_FREE_AI:
        logger.info("Will use free AI providers instead")
else:
    logger.info("GROQ API Key loaded successfully")


def initialize_free_ai():
    """Initialize free AI system on first use"""
    global free_ai_manager
    
    if free_ai_manager is not None:
        return free_ai_manager
    
    try:
        from .init_free_ai import initialize_free_ai_system
        free_ai_manager = initialize_free_ai_system()
        logger.info("✓ Free AI system initialized as fallback")
        return free_ai_manager
    except Exception as e:
        logger.error(f"Failed to initialize free AI system: {e}")
        return None


def _call_free_ai(prompt, context=None, expect_json=False):
    """Call free AI system"""
    try:
        # Initialize if needed
        if free_ai_manager is None:
            initialize_free_ai()
        
        if free_ai_manager is None:
            raise Exception("Free AI system not available")
        
        # Get response
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                free_ai_manager.get_response(
                    prompt=prompt,
                    context=context or SYSTEM_INSTRUCTION
                )
            )
        finally:
            loop.close()
        
        # Parse JSON if expected
        if expect_json:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                raise
        
        return response
        
    except Exception as e:
        logger.error(f"Free AI call failed: {e}")
        raise


def generate_response(prompt):
    """Generates a response from Grok/Free AI using REST API."""
    
    # Try primary Groq API first
    if API_KEY:
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
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Parse Grok response
            try:
                text_content = result['choices'][0]['message']['content']
                return json.loads(text_content)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse Grok response: {e}. Raw: {result}")
                # Fall through to free AI
                
        except requests.exceptions.HTTPError as e:
            # Check if rate limited
            if e.response.status_code == 429 or "rate_limit" in str(e.response.text).lower():
                logger.warning("Primary Groq API rate limited, switching to free AI...")
            else:
                logger.error(f"Grok API Error: {e}")
                # Fall through to free AI
        except Exception as e:
            logger.error(f"Grok API Error: {e}")
            # Fall through to free AI
    
    # Fallback to free AI system
    if USE_FREE_AI:
        try:
            logger.info("Using free AI providers...")
            
            # Add JSON instruction to prompt
            json_prompt = f"{prompt}\n\nIMPORTANT: Respond with ONLY a valid JSON object containing: reaction, follow_up_question, score, and feedback fields."
            
            result = _call_free_ai(json_prompt, SYSTEM_INSTRUCTION, expect_json=True)
            logger.info("✓ Free AI response received")
            return result
            
        except Exception as e:
            logger.error(f"Free AI also failed: {e}")
    
    # Ultimate fallback
    return {
        "reaction": "I see.", 
        "follow_up_question": "Could you elaborate?", 
        "score": 5, 
        "feedback": "System temporarily unavailable"
    }


def generate_text_response(prompt):
    """Generates a plain text response (non-JSON)."""
    
    # Try primary Groq API first
    if API_KEY:
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
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
                
        except Exception as e:
            logger.error(f"Grok Text API Error: {e}")
            # Fall through to free AI
    
    # Fallback to free AI
    if USE_FREE_AI:
        try:
            logger.info("Using free AI for text response...")
            response = _call_free_ai(prompt, SYSTEM_INSTRUCTION, expect_json=False)
            return response
        except Exception as e:
            logger.error(f"Free AI text response failed: {e}")
    
    return "I apologize, I'm having trouble connecting."


def generate_resume_analysis(prompt):
    """Generates a resume analysis response from Grok/Free AI."""
    
    # Try primary Groq API first
    if API_KEY:
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
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Parse Groq response
            try:
                text_content = result['choices'][0]['message']['content']
                return json.loads(text_content)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse Groq resume analysis: {e}")
                # Fall through to free AI
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"Grok API HTTP Error: {e}")
            
            # Handle rate limits gracefully
            if "rate_limit" in str(e.response.text).lower():
                logger.warning("Rate limited, trying free AI...")
                # Fall through to free AI
            else:
                return {
                    "error": "API rate limit reached",
                    "message": "Please wait a few minutes and try again.",
                    "overall_score": 70,
                    "summary": "Analysis temporarily unavailable.",
                    "factor_scores": {"impact": 70, "skills": 70, "formatting": 70, "brevity": 70},
                    "strengths": ["Unable to analyze at this time"],
                    "weaknesses": ["Please try again in a few minutes"],
                    "career_roadmap": ["Wait for API limits to reset"]
                }
        except Exception as e:
            logger.error(f"Grok Resume Analysis API Error: {e}")
            # Fall through to free AI
    
    # Fallback to free AI
    if USE_FREE_AI:
        try:
            logger.info("Using free AI for resume analysis...")
            
            # Add JSON instruction
            json_prompt = f"{prompt}\n\nIMPORTANT: Respond with ONLY a valid JSON object."
            
            result = _call_free_ai(json_prompt, expect_json=True)
            logger.info("✓ Free AI resume analysis complete")
            return result
            
        except Exception as e:
            logger.error(f"Free AI resume analysis failed: {e}")
    
    # Ultimate fallback
    return {"error": "All AI providers unavailable"}
