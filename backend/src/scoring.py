import logging
from .grok_client import generate_response
from .prompts import SCORING_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

def calculate_local_metrics(text, audio_duration=None):
    """Calculates deterministic metrics from the answer text."""
    if not text:
        return 0.0
        
    words = text.split()
    word_count = len(words)
    
    # Simple heuristics
    clarity_index = min(1.0, word_count / 20.0) # Assume 20+ words is decent length
    
    # Filler word detection
    fillers = ['um', 'uh', 'like', 'you know', 'actually', 'basically']
    filler_count = sum(1 for w in words if w.lower() in fillers)
    fluency_ratio = max(0.0, 1.0 - (filler_count / max(1, word_count)))
    
    # Pace (if audio duration is available)
    pace_score = 1.0
    if audio_duration and audio_duration > 0:
        wpm = word_count / (audio_duration / 60.0)
        # Ideal WPM 120-160
        if 120 <= wpm <= 160:
            pace_score = 1.0
        elif wpm < 100 or wpm > 180:
            pace_score = 0.7
        else:
            pace_score = 0.9
            
    # Combined local score (0-10 scale)
    local_score = (clarity_index * 0.4 + fluency_ratio * 0.4 + pace_score * 0.2) * 10
    return round(local_score, 1)

def get_semantic_score(mode, resume_summary, transcript):
    """Uses Gemini to generate a semantic score and feedback."""
    prompt = SCORING_PROMPT_TEMPLATE.format(
        mode=mode,
        resume_summary=resume_summary,
        transcript=transcript
    )
    
    response = generate_response(prompt)
    return response

def calculate_final_score(semantic_score_data, local_score):
    """Combines semantic and local scores."""
    gemini_score = semantic_score_data.get("overall_score", 0)
    
    # Weighted average: 55% Gemini, 45% Local
    final_score = (0.55 * gemini_score) + (0.45 * local_score)
    
    return {
        "final_score": round(final_score, 1),
        "gemini_score": gemini_score,
        "local_score": local_score,
        "subscores": semantic_score_data.get("subscores", {}),
        "strengths": semantic_score_data.get("strengths", []),
        "weaknesses": semantic_score_data.get("weaknesses", []),
        "improvement_plan": semantic_score_data.get("improvement_plan", []),
        "summary": semantic_score_data.get("summary", "")
    }
