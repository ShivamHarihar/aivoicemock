"""
Audio Analysis Module for Real-Time Interview Feedback
Analyzes speaking pace, fillers, confidence, and script detection
"""

import re
from collections import Counter
from datetime import datetime

class AudioAnalyzer:
    """Analyzes audio characteristics for interview feedback"""
    
    # Filler words to detect
    FILLER_WORDS = {
        'en': ['um', 'uh', 'like', 'you know', 'actually', 'basically', 'literally', 'sort of', 'kind of'],
        'hi': ['उम', 'अह', 'मतलब', 'वो', 'जैसे'],
        'mr': ['उम', 'अह', 'म्हणजे']
    }
    
    # Speaking pace thresholds (words per minute)
    PACE_THRESHOLDS = {
        'too_slow': 100,
        'slow': 120,
        'normal_min': 130,
        'normal_max': 160,
        'fast': 180,
        'too_fast': 200
    }
    
    def __init__(self, language='en'):
        self.language = language
        self.filler_words = self.FILLER_WORDS.get(language, self.FILLER_WORDS['en'])
    
    def analyze_text(self, text, duration_seconds=None):
        """
        Analyze text for speaking characteristics
        
        Args:
            text: Transcribed text
            duration_seconds: Duration of speech (optional)
            
        Returns:
            dict with analysis results
        """
        analysis = {
            'word_count': 0,
            'filler_count': 0,
            'filler_words_found': [],
            'speaking_pace': None,
            'pace_category': 'unknown',
            'confidence_score': 0,
            'confidence_level': 'unknown',
            'issues': [],
            'tips': []
        }
        
        if not text or not text.strip():
            analysis['issues'].append('No speech detected')
            return analysis
        
        # Word count
        words = text.lower().split()
        analysis['word_count'] = len(words)
        
        # Detect fillers
        filler_counter = Counter()
        for filler in self.filler_words:
            pattern = r'\b' + re.escape(filler) + r'\b'
            matches = re.findall(pattern, text.lower())
            if matches:
                filler_counter[filler] = len(matches)
        
        analysis['filler_count'] = sum(filler_counter.values())
        analysis['filler_words_found'] = [f"{word} ({count}x)" for word, count in filler_counter.most_common()]
        
        # Calculate speaking pace
        if duration_seconds and duration_seconds > 0:
            wpm = (len(words) / duration_seconds) * 60
            analysis['speaking_pace'] = round(wpm, 1)
            analysis['pace_category'] = self._categorize_pace(wpm)
        
        # Confidence scoring
        analysis['confidence_score'] = self._calculate_confidence(
            text, 
            analysis['filler_count'], 
            analysis['word_count'],
            analysis.get('speaking_pace')
        )
        analysis['confidence_level'] = self._categorize_confidence(analysis['confidence_score'])
        
        # Generate issues and tips
        analysis['issues'], analysis['tips'] = self._generate_feedback(analysis)
        
        return analysis
    
    def _categorize_pace(self, wpm):
        """Categorize speaking pace"""
        if wpm < self.PACE_THRESHOLDS['too_slow']:
            return 'too_slow'
        elif wpm < self.PACE_THRESHOLDS['slow']:
            return 'slow'
        elif wpm < self.PACE_THRESHOLDS['normal_min']:
            return 'slightly_slow'
        elif wpm <= self.PACE_THRESHOLDS['normal_max']:
            return 'normal'
        elif wpm <= self.PACE_THRESHOLDS['fast']:
            return 'slightly_fast'
        elif wpm <= self.PACE_THRESHOLDS['too_fast']:
            return 'fast'
        else:
            return 'too_fast'
    
    def _calculate_confidence(self, text, filler_count, word_count, pace):
        """
        Calculate confidence score (0-100)
        Based on: fillers, pace, sentence structure
        """
        if word_count == 0:
            return 0
        
        score = 100
        
        # Penalty for fillers (max -30)
        filler_ratio = filler_count / word_count
        score -= min(filler_ratio * 100, 30)
        
        # Penalty for pace issues (max -20)
        if pace:
            if pace < self.PACE_THRESHOLDS['too_slow'] or pace > self.PACE_THRESHOLDS['too_fast']:
                score -= 20
            elif pace < self.PACE_THRESHOLDS['slow'] or pace > self.PACE_THRESHOLDS['fast']:
                score -= 10
        
        # Penalty for very short answers (max -20)
        if word_count < 10:
            score -= 20
        elif word_count < 20:
            score -= 10
        
        # Penalty for repetition (max -15)
        unique_words = len(set(text.lower().split()))
        repetition_ratio = unique_words / word_count if word_count > 0 else 1
        if repetition_ratio < 0.5:
            score -= 15
        elif repetition_ratio < 0.7:
            score -= 7
        
        return max(0, min(100, score))
    
    def _categorize_confidence(self, score):
        """Categorize confidence level"""
        if score >= 75:
            return 'High'
        elif score >= 50:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_feedback(self, analysis):
        """Generate issues and tips based on analysis"""
        issues = []
        tips = []
        
        # Filler words feedback
        if analysis['filler_count'] > 5:
            issues.append(f"Too many filler words ({analysis['filler_count']})")
            tips.append("Try to pause instead of using filler words. Take a breath before answering.")
        elif analysis['filler_count'] > 2:
            issues.append(f"Some filler words detected ({analysis['filler_count']})")
            tips.append("Be mindful of filler words. Practice pausing naturally.")
        
        # Pace feedback
        pace_cat = analysis['pace_category']
        if pace_cat == 'too_slow':
            issues.append("Speaking too slowly")
            tips.append("Try to speak a bit faster. Show enthusiasm and energy!")
        elif pace_cat == 'too_fast':
            issues.append("Speaking too fast")
            tips.append("Slow down! Take your time to articulate clearly.")
        elif pace_cat in ['fast', 'slightly_fast']:
            tips.append("Good pace, but you could slow down slightly for clarity.")
        elif pace_cat in ['slow', 'slightly_slow']:
            tips.append("Good pace, but you could speed up slightly to show more energy.")
        
        # Length feedback
        if analysis['word_count'] < 10:
            issues.append("Answer is too short")
            tips.append("Provide more detail. Use examples to support your points.")
        elif analysis['word_count'] > 200:
            issues.append("Answer might be too long")
            tips.append("Try to be more concise. Focus on key points.")
        
        # Confidence feedback
        if analysis['confidence_level'] == 'Low':
            tips.append("Speak with more conviction. Practice your answers to build confidence.")
        elif analysis['confidence_level'] == 'Medium':
            tips.append("Good effort! Reduce fillers and maintain steady pace to boost confidence.")
        
        return issues, tips
    
    def detect_silence(self, duration_seconds):
        """
        Detect if silence is too long
        
        Args:
            duration_seconds: Duration of silence
            
        Returns:
            dict with silence analysis
        """
        result = {
            'is_too_long': False,
            'duration': duration_seconds,
            'message': None
        }
        
        if duration_seconds > 10:
            result['is_too_long'] = True
            result['message'] = "Take your time, but try to start your answer. It's okay to think out loud!"
        elif duration_seconds > 5:
            result['is_too_long'] = True
            result['message'] = "No rush! You can start whenever you're ready."
        
        return result
    
    def detect_script_reading(self, text):
        """
        Detect if answer sounds scripted or read from notes
        
        Args:
            text: Transcribed text
            
        Returns:
            dict with script detection results
        """
        indicators = {
            'overly_formal': False,
            'perfect_grammar': False,
            'unnatural_flow': False,
            'is_scripted': False,
            'confidence': 0
        }
        
        # Check for overly formal language
        formal_phrases = ['furthermore', 'moreover', 'in conclusion', 'to summarize', 'as aforementioned']
        formal_count = sum(1 for phrase in formal_phrases if phrase in text.lower())
        if formal_count > 2:
            indicators['overly_formal'] = True
        
        # Check for perfect sentence structure (too many complete sentences)
        sentences = text.split('.')
        complete_sentences = sum(1 for s in sentences if len(s.strip().split()) > 5)
        if len(sentences) > 3 and complete_sentences / len(sentences) > 0.9:
            indicators['perfect_grammar'] = True
        
        # Calculate scripted confidence
        script_score = 0
        if indicators['overly_formal']:
            script_score += 40
        if indicators['perfect_grammar']:
            script_score += 30
        
        indicators['confidence'] = script_score
        indicators['is_scripted'] = script_score > 50
        
        return indicators


# Helper function for easy integration
def analyze_answer(text, duration_seconds=None, language='en'):
    """
    Quick analysis function
    
    Args:
        text: Transcribed answer
        duration_seconds: Duration of speech
        language: Language code (en, hi, mr)
        
    Returns:
        Analysis results dict
    """
    analyzer = AudioAnalyzer(language)
    return analyzer.analyze_text(text, duration_seconds)
