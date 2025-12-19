import logging
from datetime import datetime
from .grok_client import generate_response
from .prompts import FOLLOW_UP_PROMPT_TEMPLATE, INTERVIEW_MODES, PERFORMANCE_SUMMARY_PROMPT
from .memory_store import memory
from .scoring import calculate_local_metrics

logger = logging.getLogger(__name__)

# Interview timing constants (configurable for testing)
# TEST MODE: 5-minute interview (2 min Q&A + 3 min summary)
INTERVIEW_DURATION_MINUTES = 5  # Total interview time
QA_PHASE_MINUTES = 2  # Q&A phase duration (summary triggers after this)

class InterviewEngine:
    def __init__(self):
        pass
    
    def check_interview_phase(self, session):
        """
        Check current interview phase based on elapsed time.
        Returns: ('qa', elapsed_seconds) or ('summary', elapsed_seconds)
        """
        start_time = session.get('start_time')
        if not start_time:
            return ('qa', 0)
        
        elapsed = datetime.now() - start_time
        elapsed_seconds = int(elapsed.total_seconds())
        elapsed_minutes = elapsed_seconds / 60
        
        # Check if we should transition to summary phase
        if elapsed_minutes >= QA_PHASE_MINUTES:
            return ('summary', elapsed_seconds)
        else:
            return ('qa', elapsed_seconds)
    
    def generate_performance_summary(self, session_id, elapsed_seconds):
        """
        Generate comprehensive performance summary for the interview.
        """
        session = memory.get_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        mode = session.get("mode", "HR")
        job_role = session.get("job_role", "Not specified")
        company = session.get("company", "Not specified")
        history = session.get("history", [])
        scores = session.get("scores", [])
        analyses = session.get("analyses", [])
        
        # Build transcript
        transcript = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in history])
        
        # Calculate performance metrics
        avg_local_score = sum(s.get("local_score", 0) for s in scores) / max(1, len(scores))
        avg_ai_score = sum(s.get("ai_score", 0) for s in scores) / max(1, len(scores))
        avg_confidence = sum(s.get("confidence_score", 0) for s in scores) / max(1, len(scores))
        
        performance_metrics = f"""Average Scores:
- Local Score: {avg_local_score:.1f}/10
- AI Score: {avg_ai_score:.1f}/10
- Confidence: {avg_confidence:.1f}/100
- Total Questions: {len([h for h in history if h['role'] == 'ai'])}
- Total Responses: {len([h for h in history if h['role'] == 'user'])}
"""
        
        # Generate summary using AI
        prompt = PERFORMANCE_SUMMARY_PROMPT.format(
            mode=INTERVIEW_MODES.get(mode, "Standard Interview"),
            job_role=job_role,
            company=company,
            duration_minutes=int(elapsed_seconds / 60),
            transcript=transcript,
            performance_metrics=performance_metrics
        )
        
        # TODO: Fix AI summary generation - generate_response doesn't support expect_json parameter
        # For now, use fallback summary
        summary_text = None
        
        # If AI fails, provide a basic summary
        if not summary_text:
            summary_text = f"""Thank you for completing this {mode} interview. 

Your overall performance was good with an average score of {avg_local_score:.1f} out of 10. 
You demonstrated {avg_confidence:.0f}% confidence throughout the interview.

Key areas to focus on for improvement:
1. Practice articulating your thoughts more clearly
2. Provide more specific examples from your experience
3. Work on reducing filler words and pauses

Keep practicing and you'll continue to improve. Best of luck in your job search!"""
        
        # Update memory
        memory.add_history(session_id, "ai", summary_text)
        memory.update_session(session_id, "interview_phase", "completed")
        
        return {
            "full_text": summary_text,
            "phase": "summary",
            "interview_complete": True,
            "elapsed_seconds": elapsed_seconds
        }

    def process_answer(self, session_id, user_audio_text, audio_duration=None):
        """
        Main logic pipeline with real-time analysis:
        1. Retrieve session context.
        2. Analyze audio for mistakes and confidence.
        3. Calculate local metrics for the answer.
        4. Send context + answer to AI for analysis & next question.
        5. Update session state (difficulty, history).
        6. Return AI response (text) for TTS with real-time feedback.
        """
        from .audio_analyzer import analyze_answer
        from .mistake_detector import analyze_mistakes
        from .question_packs import get_company_style_prompt, get_questions_for_role
        
        session = memory.get_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        # Check interview phase
        phase, elapsed_seconds = self.check_interview_phase(session)
        
        # If we've reached summary phase, generate performance summary
        if phase == 'summary' and session.get('interview_phase') != 'summary':
            memory.update_session(session_id, 'interview_phase', 'summary')
            return self.generate_performance_summary(session_id, elapsed_seconds)

        mode = session.get("mode", "HR")
        job_role = session.get("job_role", "")
        company = session.get("company", "")
        history = session.get("history", [])
        resume_context = session.get("resume_context", {})
        last_question = history[-1]['content'] if history and history[-1]['role'] == 'ai' else "Tell me about yourself"
        
        # Real-time audio analysis
        audio_analysis = analyze_answer(user_audio_text, audio_duration, language='en')
        
        # Mistake detection
        mistake_analysis = analyze_mistakes(last_question, user_audio_text, audio_duration)
        
        # Store analysis in session
        if 'analyses' not in session:
            session['analyses'] = []
        session['analyses'].append({
            'audio': audio_analysis,
            'mistakes': mistake_analysis,
            'timestamp': str(datetime.now())
        })
        
        # 1. Local Metrics
        local_score = calculate_local_metrics(user_audio_text, audio_duration)
        
        # Adjust score based on confidence and mistakes
        adjusted_score = local_score
        adjusted_score += (audio_analysis['confidence_score'] / 100) * 2  # Max +2 for high confidence
        adjusted_score -= len(mistake_analysis['all_feedback']) * 0.5  # -0.5 per mistake
        adjusted_score = max(0, min(10, adjusted_score))
        
        # 2. Construct Prompt with real-time feedback + role/company context + resume context
        history_summary = "\n".join([f"{h['role']}: {h['content']}" for h in history[-6:]])
        
        # Add role context
        role_context = ""
        role_specific_guidance = ""
        if job_role:
            role_context = f"**Job Role**: {job_role}\n"
            sample_questions = get_questions_for_role(job_role, 3)
            if sample_questions:
                role_specific_guidance = f"- Ask questions relevant to {job_role} role\n- Example topics: {', '.join(sample_questions[:2])}"
        
        # Add company context
        company_context = ""
        company_specific_guidance = ""
        if company:
            company_prompt = get_company_style_prompt(company)
            if company_prompt:
                company_context = company_prompt
                company_specific_guidance = f"- Follow {company}'s interview style and principles"
        
        # Add resume context with detailed information
        resume_context_str = ""
        topic_tracking_str = ""
        topics_covered_str = "None yet"
        total_questions = session.get('total_questions_asked', 0)
        max_questions = 12
        
        if resume_context:
            candidate_name = resume_context.get('candidate_name', 'Candidate')
            skills = resume_context.get('skills', [])
            projects = resume_context.get('projects', [])
            experience = resume_context.get('experience', [])
            education = resume_context.get('education', [])
            
            # Build detailed resume context
            resume_context_str = f"""
**📋 CANDIDATE'S RESUME DETAILS:**
- **Name**: {candidate_name}

**💼 WORK EXPERIENCE / INTERNSHIPS:**
{chr(10).join([f"  • {exp}" for exp in experience[:5]]) if experience else "  • Not specified"}

**🚀 PROJECTS:**
{chr(10).join([f"  • {proj}" for proj in projects[:5]]) if projects else "  • Not specified"}

**🎓 EDUCATION:**
{chr(10).join([f"  • {edu}" for edu in education[:3]]) if education else "  • Not specified"}

**🛠️ TECHNICAL SKILLS:**
  • {', '.join(skills[:15]) if skills else 'Not specified'}

**⚠️ IMPORTANT**: Ask questions about the SPECIFIC items listed above (use exact project names, company names, technologies)
"""
        
        # Topic tracking with resume section awareness
        topic_question_count = session.get('topic_question_count', {})
        resume_topics = session.get('resume_topics', [])
        
        # Track resume section coverage
        section_coverage = {
            'projects': 0,
            'experience': 0,
            'education': 0,
            'skills': 0
        }
        
        # Count questions per section
        for topic, count in topic_question_count.items():
            if 'project:' in topic:
                section_coverage['projects'] += count
            elif 'experience:' in topic:
                section_coverage['experience'] += count
            elif 'education:' in topic:
                section_coverage['education'] += count
            elif 'skill:' in topic:
                section_coverage['skills'] += count
        
        if topic_question_count:
            # Find topics that have been covered
            covered_topics = [topic for topic, count in topic_question_count.items() if count > 0]
            exhausted_topics = [topic for topic, count in topic_question_count.items() if count >= 2]
            available_topics = [topic for topic in resume_topics if topic_question_count.get(topic, 0) < 2]
            
            if covered_topics:
                topics_covered_str = ', '.join([t.split(':')[1][:30] for t in covered_topics[:5]])
            
            # Build section-aware topic tracking
            uncovered_sections = []
            if section_coverage['projects'] == 0 and projects:
                uncovered_sections.append('PROJECTS (PRIORITY!)')
            if section_coverage['experience'] == 0 and experience:
                uncovered_sections.append('EXPERIENCE/INTERNSHIPS (PRIORITY!)')
            if section_coverage['education'] == 0 and education:
                uncovered_sections.append('EDUCATION (PRIORITY!)')
            
            # Build exhausted topics warning
            exhausted_list = []
            for topic, count in topic_question_count.items():
                if count >= 2:
                    # Extract readable name from topic
                    topic_name = topic.split(':')[1] if ':' in topic else topic
                    exhausted_list.append(f"{topic_name} ({count} questions)")
            
            exhausted_warning = ""
            if exhausted_list:
                exhausted_warning = f"""
**🚫 EXHAUSTED TOPICS - DO NOT ASK ABOUT THESE:**
{chr(10).join([f"  ❌ {topic}" for topic in exhausted_list[:5]])}
**⚠️ These topics have reached the 2-question limit. You MUST ask about different topics.**
"""
            
            topic_tracking_str = f"""
{exhausted_warning}
**📊 RESUME SECTION COVERAGE:**
- Projects: {section_coverage['projects']} questions asked
- Experience/Internships: {section_coverage['experience']} questions asked
- Education: {section_coverage['education']} questions asked
- Skills: {section_coverage['skills']} questions asked

**🎯 NEXT QUESTION SHOULD FOCUS ON:**
{chr(10).join([f"  • {section}" for section in uncovered_sections]) if uncovered_sections else "  • Continue with available topics (avoid exhausted ones)"}

**Topic Details:**
- Topics exhausted (2+ questions): {len(exhausted_topics)}
- Topics available: {len(available_topics)}
"""
        
        # Add real-time feedback to prompt
        feedback_context = f"""
Real-time Analysis:
- Confidence: {audio_analysis['confidence_level']}
- Speaking Pace: {audio_analysis.get('speaking_pace', 'N/A')} WPM ({audio_analysis['pace_category']})
- Filler Words: {audio_analysis['filler_count']}
- Issues Detected: {', '.join(mistake_analysis['all_feedback']) if mistake_analysis['all_feedback'] else 'None'}
"""
        
        prompt = FOLLOW_UP_PROMPT_TEMPLATE.format(
            mode=INTERVIEW_MODES.get(mode, "Standard Interview"),
            role_context=role_context,
            company_context=company_context,
            resume_context=resume_context_str,
            total_questions=total_questions,
            max_questions=max_questions,
            topics_covered=topics_covered_str,
            topic_tracking=topic_tracking_str,
            role_specific_guidance=role_specific_guidance,
            company_specific_guidance=company_specific_guidance,
            history=history_summary + "\n" + feedback_context,
            last_answer=user_audio_text,
            multilingual_note="**IMPORTANT**: If the candidate responds in Hindi or Marathi, respond in the SAME language."
        )
        
        # 3. AI Call
        ai_data = generate_response(prompt)
        
        # Mock Mode Fallback
        if ai_data.get("reaction") == "Error" or "API Key missing" in ai_data.get("follow_up_question", ""):
            import random
            
            # Use role-specific questions if available
            if job_role:
                role_questions = get_questions_for_role(job_role, 5)
                mock_questions = role_questions if role_questions else [
                    "Could you tell me more about your experience?",
                    "What was the most challenging project you've worked on?",
                ]
            else:
                mock_questions = [
                    "Could you tell me more about your experience?",
                    "What was the most challenging project you've worked on?",
                    "How do you handle tight deadlines?",
                ]
            
            mock_reactions = ["I see.", "That's interesting.", "Okay, understood.", "Thanks for sharing that."]
            
            ai_data = {
                "reaction": random.choice(mock_reactions),
                "follow_up_question": random.choice(mock_questions),
                "score": adjusted_score,
                "feedback": "Mock mode active"
            }
        
        # Add gentle real-time tips to AI response
        real_time_tips = []
        if audio_analysis['tips']:
            real_time_tips.append(audio_analysis['tips'][0])  # Add one tip
        
        # 4. Build full response
        full_text = ai_data.get("reaction", "I see.")
        
        # Add gentle tip if needed
        if real_time_tips and audio_analysis['confidence_level'] != 'High':
            full_text += f" Quick tip: {real_time_tips[0]}"
        
        full_text += " " + ai_data.get("follow_up_question", "Can you tell me more?")
        
        # 5. Update Memory
        memory.add_history(session_id, "user", user_audio_text)
        memory.add_history(session_id, "ai", full_text)
        memory.add_score(session_id, {
            "local_score": adjusted_score,
            "ai_score": ai_data.get("score", 5),
            "confidence_score": audio_analysis['confidence_score'],
            "feedback": ai_data.get("feedback", "")
        })
        
        
        # Update topic tracking with improved matching
        current_topic = ai_data.get("topic", "")
        if current_topic:
            resume_topics = session.get('resume_topics', [])
            topic_question_count = session.get('topic_question_count', {})
            
            # Normalize the current topic format (ensure it has category:name format)
            if ':' not in current_topic:
                # If AI didn't use proper format, try to infer it
                logger.warning(f"Topic missing category prefix: {current_topic}")
                current_topic = f"general:{current_topic}"
            
            # Extract category and name from current topic
            current_category = current_topic.split(':')[0].lower()
            current_name = current_topic.split(':')[1].lower() if ':' in current_topic else current_topic.lower()
            
            matched = False
            # Try exact or close matching with resume topics
            for resume_topic in resume_topics:
                if ':' not in resume_topic:
                    continue
                    
                resume_category = resume_topic.split(':')[0].lower()
                resume_name = resume_topic.split(':')[1].lower()
                
                # Match if same category and similar name (at least 50% overlap)
                if resume_category == current_category:
                    # Check for substring match or significant word overlap
                    if (current_name in resume_name or resume_name in current_name or
                        len(set(current_name.split()) & set(resume_name.split())) >= 2):
                        # Increment count for this specific resume topic
                        topic_question_count[resume_topic] = topic_question_count.get(resume_topic, 0) + 1
                        memory.update_session(session_id, 'topic_question_count', topic_question_count)
                        logger.info(f"✅ Matched topic '{current_topic}' to '{resume_topic}' - Count: {topic_question_count[resume_topic]}")
                        
                        # Warn if limit reached
                        if topic_question_count[resume_topic] >= 2:
                            logger.warning(f"⚠️ Topic '{resume_topic}' has reached limit (2 questions). Should move to next topic.")
                        
                        matched = True
                        break
            
            if not matched:
                # Track as new topic if not matched
                topic_question_count[current_topic] = topic_question_count.get(current_topic, 0) + 1
                memory.update_session(session_id, 'topic_question_count', topic_question_count)
                logger.info(f"📝 New topic tracked: '{current_topic}' - Count: {topic_question_count[current_topic]}")
        
        # Increment total questions asked
        total_questions = session.get('total_questions_asked', 0) + 1
        memory.update_session(session_id, 'total_questions_asked', total_questions)
        logger.info(f"Total questions asked: {total_questions}")
        
        # Check if we've reached the question limit (10-12 questions)
        if total_questions >= 10:
            logger.info(f"Reached question limit ({total_questions} questions). Consider wrapping up.")
            # Note: We don't force summary here, let the time-based trigger handle it
            # But we could add a flag to indicate interview should wrap up soon
        
        # Get elapsed time for frontend timer
        _, elapsed_seconds = self.check_interview_phase(session)
        
        return {
            "full_text": full_text,
            "difficulty": session.get("difficulty", "Normal"),
            "phase": "qa",
            "elapsed_seconds": elapsed_seconds,
            "real_time_feedback": {
                "confidence": audio_analysis['confidence_level'],
                "pace": audio_analysis['pace_category'],
                "filler_count": audio_analysis['filler_count'],
                "tips": audio_analysis['tips'][:2],  # Max 2 tips
                "issues": audio_analysis['issues']
            }
        }

# Global instance
engine = InterviewEngine()
