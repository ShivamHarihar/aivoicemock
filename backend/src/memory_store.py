import logging

logger = logging.getLogger(__name__)

class MemoryStore:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        """Initialize a new session."""
        from datetime import datetime
        self.sessions[session_id] = {
            "created_at": None,
            "start_time": datetime.now(),  # Track interview start time
            "interview_phase": "qa",  # 'qa' or 'summary'
            "history": [],
            "resume_context": {},
            "mode": "HR",
            "difficulty": 1,
            "scores": [],
            "emotional_state": "neutral",
            "metadata": {},
            # New fields for resume-based personalized interviews
            "candidate_name": None,
            "resume_topics": [],
            "topic_question_count": {},  # Track questions asked per topic
            "total_questions_asked": 0,  # Total questions counter
        }
        logger.info(f"Session {session_id} created.")

    def get_session(self, session_id):
        """Retrieve session data."""
        return self.sessions.get(session_id)

    def update_session(self, session_id, key, value):
        """Update a specific key in the session."""
        if session_id in self.sessions:
            self.sessions[session_id][key] = value
            return True
        return False

    def add_history(self, session_id, role, content):
        """Add a message to the conversation history."""
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "role": role,
                "content": content
            })
    
    def add_score(self, session_id, score_data):
        """Add a score entry to the session."""
        if session_id in self.sessions:
            if "scores" not in self.sessions[session_id]:
                self.sessions[session_id]["scores"] = []
            self.sessions[session_id]["scores"].append(score_data)

    def delete_session(self, session_id):
        """Remove a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session {session_id} deleted.")

# Global instance
memory = MemoryStore()
