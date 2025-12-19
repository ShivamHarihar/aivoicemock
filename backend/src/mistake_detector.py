"""
Mistake Detection Module
Detects rambling, off-topic answers, and provides content analysis
"""

import re
from .groq_client import generate_text_response

class MistakeDetector:
    """Detects common interview mistakes in answers"""
    
    def __init__(self):
        self.rambling_threshold = 150  # words
        self.min_relevance_score = 0.6
    
    def detect_rambling(self, text):
        """
        Detect if answer is rambling or unfocused
        
        Args:
            text: Answer text
            
        Returns:
            dict with rambling analysis
        """
        result = {
            'is_rambling': False,
            'word_count': 0,
            'repetition_score': 0,
            'focus_score': 0,
            'feedback': None
        }
        
        words = text.split()
        result['word_count'] = len(words)
        
        # Check length
        if len(words) > self.rambling_threshold:
            result['is_rambling'] = True
            result['feedback'] = "Your answer is quite long. Try to be more concise and focus on key points."
            return result
        
        # Check for repetition
        unique_words = set(words)
        repetition_ratio = len(unique_words) / len(words) if words else 1
        result['repetition_score'] = round(repetition_ratio, 2)
        
        if repetition_ratio < 0.5:
            result['is_rambling'] = True
            result['feedback'] = "You're repeating yourself. Try to organize your thoughts before answering."
            return result
        
        # Check for circular logic (same concepts repeated)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) > 3:
            # Simple check: if sentences are very similar in length and structure
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            similar_length = sum(1 for s in sentences if abs(len(s.split()) - avg_length) < 3)
            if similar_length / len(sentences) > 0.7:
                result['focus_score'] = 0.4
                result['feedback'] = "Try to vary your sentence structure and add new information in each point."
        
        return result
    
    def check_relevance(self, question, answer):
        """
        Check if answer is relevant to the question
        Uses AI to determine relevance
        
        Args:
            question: Interview question
            answer: User's answer
            
        Returns:
            dict with relevance analysis
        """
        result = {
            'is_relevant': True,
            'relevance_score': 1.0,
            'feedback': None
        }
        
        # Quick checks
        if len(answer.split()) < 5:
            result['is_relevant'] = False
            result['relevance_score'] = 0.2
            result['feedback'] = "Your answer is too short. Please provide more detail."
            return result
        
        # Use AI to check relevance
        prompt = f"""
        Question: {question}
        Answer: {answer}
        
        Is this answer relevant and on-topic? Rate relevance from 0.0 to 1.0.
        If relevance < 0.6, the answer is off-topic.
        
        Respond with ONLY a number between 0.0 and 1.0.
        """
        
        try:
            response = generate_text_response(prompt)
            score = float(response.strip())
            result['relevance_score'] = max(0.0, min(1.0, score))
            
            if result['relevance_score'] < self.min_relevance_score:
                result['is_relevant'] = False
                result['feedback'] = "Your answer seems off-topic. Make sure to directly address the question asked."
        except:
            # If AI check fails, assume relevant
            pass
        
        return result
    
    def analyze_structure(self, text):
        """
        Analyze answer structure and organization
        
        Args:
            text: Answer text
            
        Returns:
            dict with structure analysis
        """
        result = {
            'has_structure': False,
            'has_introduction': False,
            'has_examples': False,
            'has_conclusion': False,
            'feedback': []
        }
        
        text_lower = text.lower()
        
        # Check for introduction phrases
        intro_phrases = ['first', 'to begin', 'let me start', 'i would say', 'in my experience']
        result['has_introduction'] = any(phrase in text_lower for phrase in intro_phrases)
        
        # Check for examples
        example_phrases = ['for example', 'for instance', 'such as', 'like when', 'in one case']
        result['has_examples'] = any(phrase in text_lower for phrase in example_phrases)
        
        # Check for conclusion
        conclusion_phrases = ['in conclusion', 'to summarize', 'overall', 'in the end', 'finally']
        result['has_conclusion'] = any(phrase in text_lower for phrase in conclusion_phrases)
        
        # Overall structure check
        structure_count = sum([result['has_introduction'], result['has_examples'], result['has_conclusion']])
        result['has_structure'] = structure_count >= 2
        
        # Generate feedback
        if not result['has_examples']:
            result['feedback'].append("Try to include specific examples to support your points.")
        
        if not result['has_structure']:
            result['feedback'].append("Structure your answer: Start with a clear point, provide examples, and conclude.")
        
        return result
    
    def detect_all_mistakes(self, question, answer, duration_seconds=None):
        """
        Comprehensive mistake detection
        
        Args:
            question: Interview question
            answer: User's answer
            duration_seconds: Duration of answer (optional)
            
        Returns:
            dict with all detected mistakes and feedback
        """
        mistakes = {
            'rambling': self.detect_rambling(answer),
            'relevance': self.check_relevance(question, answer),
            'structure': self.analyze_structure(answer),
            'all_feedback': [],
            'severity': 'none'  # none, low, medium, high
        }
        
        # Collect all feedback
        if mistakes['rambling']['feedback']:
            mistakes['all_feedback'].append(mistakes['rambling']['feedback'])
        
        if mistakes['relevance']['feedback']:
            mistakes['all_feedback'].append(mistakes['relevance']['feedback'])
        
        if mistakes['structure']['feedback']:
            mistakes['all_feedback'].extend(mistakes['structure']['feedback'])
        
        # Determine severity
        issue_count = len(mistakes['all_feedback'])
        if issue_count == 0:
            mistakes['severity'] = 'none'
        elif issue_count == 1:
            mistakes['severity'] = 'low'
        elif issue_count == 2:
            mistakes['severity'] = 'medium'
        else:
            mistakes['severity'] = 'high'
        
        return mistakes


# Helper function
def analyze_mistakes(question, answer, duration_seconds=None):
    """
    Quick mistake analysis
    
    Args:
        question: Interview question
        answer: User's answer
        duration_seconds: Duration of answer
        
    Returns:
        Mistake analysis dict
    """
    detector = MistakeDetector()
    return detector.detect_all_mistakes(question, answer, duration_seconds)
