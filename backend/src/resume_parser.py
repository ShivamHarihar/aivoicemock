import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def extract_candidate_info(resume_text: str) -> Dict:
    """
    Extract structured information from resume text.
    
    Args:
        resume_text: Raw text content from resume
        
    Returns:
        Dictionary containing:
        - candidate_name: Extracted name
        - skills: List of technical skills
        - projects: List of project names/descriptions
        - experience: List of work experience items
        - education: Education information
        - topics: List of interview topics derived from resume
    """
    if not resume_text or len(resume_text.strip()) < 50:
        logger.warning("Resume text too short or empty")
        return {
            "candidate_name": None,
            "skills": [],
            "projects": [],
            "experience": [],
            "education": [],
            "topics": []
        }
    
    result = {
        "candidate_name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text),
        "projects": extract_projects(resume_text),
        "experience": extract_experience(resume_text),
        "education": extract_education(resume_text),
        "topics": []
    }
    
    # Generate interview topics from extracted information
    result["topics"] = identify_topics(result)
    
    logger.info(f"Extracted candidate info: Name={result['candidate_name']}, "
                f"Skills={len(result['skills'])}, Projects={len(result['projects'])}, "
                f"Topics={len(result['topics'])}")
    
    return result


def extract_name(text: str) -> Optional[str]:
    """
    Extract candidate name from resume text.
    Assumes name is typically at the beginning of the resume.
    """
    lines = text.strip().split('\n')
    
    # Try first few lines for name
    for line in lines[:5]:
        line = line.strip()
        if not line:
            continue
            
        # Skip common headers
        if any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'contact']):
            continue
            
        # Check if line looks like a name (2-4 words, mostly alphabetic)
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if mostly alphabetic
            if all(word.replace('.', '').replace(',', '').isalpha() for word in words):
                return line
    
    # Fallback: look for "Name:" pattern
    name_match = re.search(r'(?:Name|Full Name|Candidate)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text, re.IGNORECASE)
    if name_match:
        return name_match.group(1).strip()
    
    return None


def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from resume text.
    """
    skills = []
    
    # Common skill keywords and technologies
    skill_patterns = [
        # Programming languages
        r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|Go|Rust|Swift|Kotlin|PHP|R|MATLAB|Scala)\b',
        # Frameworks
        r'\b(React|Angular|Vue|Django|Flask|FastAPI|Spring|Node\.js|Express|TensorFlow|PyTorch|Keras|Scikit-learn)\b',
        # Databases
        r'\b(MySQL|PostgreSQL|MongoDB|Redis|Cassandra|Oracle|SQL Server|DynamoDB|Elasticsearch)\b',
        # Cloud & DevOps
        r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|CI/CD|Terraform|Ansible)\b',
        # Data Science & ML
        r'\b(Machine Learning|Deep Learning|NLP|Computer Vision|Data Analysis|Pandas|NumPy|Matplotlib)\b',
        # Other technologies
        r'\b(REST API|GraphQL|Microservices|Agile|Scrum|Linux|Unix|Bash)\b'
    ]
    
    # Look for skills section
    skills_section = re.search(r'(?:Skills|Technical Skills|Technologies|Expertise)\s*:?\s*\n((?:.+\n?)+?)(?:\n\n|$)', 
                               text, re.IGNORECASE | re.MULTILINE)
    
    search_text = skills_section.group(1) if skills_section else text
    
    # Extract skills using patterns
    for pattern in skill_patterns:
        matches = re.finditer(pattern, search_text, re.IGNORECASE)
        for match in matches:
            skill = match.group(1)
            if skill not in skills:
                skills.append(skill)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills[:15]  # Limit to top 15 skills


def extract_projects(text: str) -> List[str]:
    """
    Extract project names and descriptions from resume.
    """
    projects = []
    
    # Look for projects section
    projects_section = re.search(r'(?:Projects|Personal Projects|Academic Projects)\s*:?\s*\n((?:.+\n?)+?)(?:\n\n|Experience|Education|$)', 
                                 text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if projects_section:
        project_text = projects_section.group(1)
        
        # Split by bullet points or numbered lists
        project_items = re.split(r'\n\s*[-•*]\s*|\n\s*\d+\.\s*', project_text)
        
        for item in project_items:
            item = item.strip()
            if len(item) > 10 and len(item) < 500:  # Reasonable project description length
                # Take first line or first sentence as project name
                first_line = item.split('\n')[0].strip()
                if first_line:
                    projects.append(first_line[:200])  # Limit length
    
    return projects[:5]  # Limit to top 5 projects


def extract_experience(text: str) -> List[str]:
    """
    Extract work experience items from resume.
    """
    experience = []
    
    # Look for experience section
    exp_section = re.search(r'(?:Experience|Work Experience|Professional Experience|Employment)\s*:?\s*\n((?:.+\n?)+?)(?:\n\n|Projects|Education|Skills|$)', 
                           text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if exp_section:
        exp_text = exp_section.group(1)
        
        # Look for company names and job titles (typically in bold or at start of line)
        job_patterns = [
            r'([A-Z][A-Za-z\s&]+(?:Inc|LLC|Ltd|Corporation|Corp)?)\s*[-–|]\s*([A-Z][A-Za-z\s]+)',  # Company - Title
            r'([A-Z][A-Za-z\s]+)\s+at\s+([A-Z][A-Za-z\s&]+)',  # Title at Company
        ]
        
        for pattern in job_patterns:
            matches = re.finditer(pattern, exp_text)
            for match in matches:
                exp_item = f"{match.group(1)} - {match.group(2)}"
                if exp_item not in experience:
                    experience.append(exp_item)
    
    return experience[:5]  # Limit to top 5 experiences


def extract_education(text: str) -> List[str]:
    """
    Extract education information from resume.
    """
    education = []
    
    # Look for education section
    edu_section = re.search(r'(?:Education|Academic Background|Qualifications)\s*:?\s*\n((?:.+\n?)+?)(?:\n\n|Experience|Projects|Skills|$)', 
                           text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if edu_section:
        edu_text = edu_section.group(1)
        
        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|B\.Tech|M\.Tech|B\.S|M\.S|MBA).*?(?:in|of)\s+([A-Za-z\s]+)',
            r'(B\.E|M\.E|B\.Sc|M\.Sc).*?(?:in|of)?\s+([A-Za-z\s]+)',
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, edu_text, re.IGNORECASE)
            for match in matches:
                edu_item = f"{match.group(1)} in {match.group(2)}"
                if edu_item not in education:
                    education.append(edu_item.strip())
    
    return education[:3]  # Limit to top 3 education items


def identify_topics(resume_context: Dict) -> List[str]:
    """
    Create a list of interview topics from resume context.
    Topics are derived from skills, projects, and experience.
    
    Args:
        resume_context: Dictionary with extracted resume information
        
    Returns:
        List of topic strings for interview questions
    """
    topics = []
    
    # Add skills as topics (group similar skills)
    skills = resume_context.get('skills', [])
    for skill in skills[:10]:  # Top 10 skills
        topics.append(f"skill:{skill}")
    
    # Add projects as topics
    projects = resume_context.get('projects', [])
    for i, project in enumerate(projects[:3]):  # Top 3 projects
        # Extract key words from project name
        project_name = project.split('\n')[0][:50]  # First line, max 50 chars
        topics.append(f"project:{project_name}")
    
    # Add experience domains as topics
    experience = resume_context.get('experience', [])
    for exp in experience[:3]:  # Top 3 experiences
        topics.append(f"experience:{exp[:50]}")
    
    # Add education as topic if available
    education = resume_context.get('education', [])
    if education:
        topics.append(f"education:{education[0][:50]}")
    
    return topics


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from resume text.
    """
    # Standard email regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    if match:
        return match.group(0)
    return None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from resume text.
    Handles various formats: +1-234-567-8900, (123) 456-7890, 123 456 7890, etc.
    """
    # Regex for phone numbers - simplistic but covers common cases
    # Look for patterns with at least 10 digits, possibly separated by -, space, or .
    # It might start with a +
    
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    # Iterate through matches and pick the first reasonable one
    matches = re.finditer(phone_pattern, text)
    for match in matches:
        phone = match.group(0)
        # minimal validation: ensure it has at least 10 digits
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            return phone.strip()
            
    return None
