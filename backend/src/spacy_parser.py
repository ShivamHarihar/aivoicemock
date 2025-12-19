import logging
import re

logger = logging.getLogger(__name__)

try:
    import spacy
except ImportError:
    spacy = None
    logger.warning("SpaCy not installed. Resume parsing will be limited.")

# Load English tokenizer, tagger, parser and NER
nlp = None
if spacy:
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("SpaCy model loaded.")
    except OSError:
        logger.warning("SpaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'.")
        nlp = None
else:
    logger.warning("SpaCy module not available, parsing disabled.")

def parse_resume(text):
    """Extracts skills, education, and experience from resume text."""
    if not nlp:
        return {}

    doc = nlp(text)
    
    # Simple extraction logic (can be enhanced with specialized NER models)
    skills = []
    education = []
    experience = []
    
    # Heuristic extraction based on common keywords and entities
    # This is a basic implementation. Production systems use trained NER models for resumes.
    
    for ent in doc.ents:
        if ent.label_ == "ORG":
            experience.append(ent.text)
        elif ent.label_ == "DATE":
            # Could be associated with education or experience
            pass
            
    # Keyword matching for common tech skills
    common_skills = ["python", "java", "c++", "javascript", "react", "flask", "aws", "docker", "kubernetes", "sql", "nosql", "git", "communication", "leadership"]
    
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            skills.append(skill.capitalize())
            
    return {
        "skills": list(set(skills)),
        "experience": list(set(experience)), # Deduplicate
        "education": education # Placeholder for more complex logic
    }
