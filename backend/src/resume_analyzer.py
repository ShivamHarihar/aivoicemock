import os
import json
import logging
from pypdf import PdfReader
from .grok_client import generate_resume_analysis
from .prompts import DETAILED_RESUME_ANALYSIS_PROMPT
from .resume_parser import extract_candidate_info

logger = logging.getLogger(__name__)

def parse_resume(filepath):
    """Extracts text from a PDF or TXT file."""
    try:
        ext = os.path.splitext(filepath)[1].lower()
        text = ""
        
        if ext == '.pdf':
            try:
                reader = PdfReader(filepath)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"Error reading PDF: {e}")
                return None
        elif ext == '.txt':
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception as e:
                logger.error(f"Error reading TXT: {e}")
                return None
        else:
            return None
            
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing resume: {e}")
        return None

def analyze_resume_content(text):
    """Analyzes resume text using Gemini and returns a structured JSON response."""
    if not text or len(text) < 50:
        return {"error": "Resume content is too short or empty."}
        
    try:
        prompt = DETAILED_RESUME_ANALYSIS_PROMPT.format(resume_text=text[:15000]) # Limit context
        response = generate_resume_analysis(prompt)
        
        logger.info(f"Gemini response type: {type(response)}")
        logger.info(f"Gemini response keys: {response.keys() if isinstance(response, dict) else 'not a dict'}")
        
        # Check if it's an error response
        if isinstance(response, dict) and "error" in response:
            return response
        
        # generate_response already returns parsed JSON
        if isinstance(response, dict):
            # Check if it's an error response from the interview system
            if "reaction" in response:
                logger.warning("Received interview-style response instead of resume analysis")
                return {"error": "AI returned unexpected format. Please try again."}
            
            # Extract structured data from resume (Regex fallback)
            regex_data = extract_candidate_info(text)
            
            # Extract structured data from AI response
            ai_data = response.get("structured_data", {})
            personal_info = ai_data.get("personal_info", {})
            
            # Helper to prefer AI data over Regex data
            def get_best(ai_val, regex_val):
                return ai_val if ai_val and str(ai_val).strip() != "" else regex_val

            # Provide defaults for missing fields to be more lenient
            result = {
                "overall_score": response.get("overall_score", 70),
                "summary": response.get("summary", "Resume analysis completed."),
                "factor_scores": response.get("factor_scores", {
                    "impact": 70,
                    "skills": 70,
                    "formatting": 70,
                    "brevity": 70
                }),
                "strengths": response.get("strengths", ["Professional experience", "Technical skills", "Clear structure"]),
                "weaknesses": response.get("weaknesses", ["Could add more quantifiable achievements", "Consider adding a summary section"]),
                "career_roadmap": response.get("career_roadmap", ["Continue building technical skills", "Seek leadership opportunities", "Network in your industry"]),
                "section_feedback": response.get("section_feedback", []),
                "resume_text": text,  # Include original text for recreation
                
                # Merge structured data (AI > Regex)
                "candidate_name": get_best(personal_info.get("name"), regex_data.get("candidate_name")),
                "email": get_best(personal_info.get("email"), regex_data.get("email")),
                "phone": get_best(personal_info.get("phone"), regex_data.get("phone")),
                "linkedin": personal_info.get("linkedin"),
                "location": personal_info.get("location"),
                
                # Complex structures
                "extracted_skills": ai_data.get("skills", regex_data.get("skills", [])),
                "extracted_experience": ai_data.get("experience", regex_data.get("experience", [])),
                "extracted_projects": ai_data.get("projects", regex_data.get("projects", [])),
                "extracted_education": ai_data.get("education", regex_data.get("education", [])),
                
                # Raw structured data for frontend if needed
                "structured_resume": ai_data
            }
            
            return result
        
        return {"error": "Failed to parse AI response."}
        
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        return {"error": str(e)}

