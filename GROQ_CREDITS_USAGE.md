# Groq API Credits Usage - AI Interview System

## Overview
This document details all the Groq API credit consumption points in the AI Interview functionality. The system uses **Groq API** with the `llama-3.3-70b-versatile` model for all AI-powered features.

---

## API Configuration

**Model Used:** `llama-3.3-70b-versatile`  
**API Endpoint:** `https://api.groq.com/openai/v1/chat/completions`  
**Temperature:** `0.7` (for all requests)  
**API Key:** `GROQ_API_KEY` (from environment variables)

---

## Credit Consumption Points

### 1. **Interview Question Generation & Follow-ups** 🎯
**File:** `backend/src/grok_client.py` → `generate_response()`  
**Called by:** `backend/src/interview_engine.py` → `process_answer()`

**Frequency:** Every time the candidate answers a question (typically 10-12 times per interview)

**Request Details:**
- **System Prompt:** Interview mode instructions (HR/Technical/Managerial/Behavioral)
- **User Prompt:** Includes:
  - Conversation history (last 6 exchanges)
  - Candidate's resume context (skills, projects, experience, education)
  - Job role and company context
  - Topic tracking information
  - Real-time audio analysis feedback
  - Performance metrics
- **Response Format:** JSON with structured output
  ```json
  {
    "reaction": "Brief natural reaction",
    "follow_up_question": "Next interview question",
    "score": 1-10,
    "feedback": "Internal note",
    "topic": "category:name"
  }
  ```

**Estimated Token Usage per Call:**
- Input: ~1,500-2,500 tokens (depending on conversation history and resume length)
- Output: ~100-200 tokens
- **Total per question:** ~1,700-2,700 tokens

**Total for Interview (10-12 questions):**
- **~17,000-32,400 tokens per interview session**

---

### 2. **Interview Greeting Generation** 👋
**File:** `backend/src/grok_client.py` → `generate_text_response()`  
**Called by:** `backend/app/app.py` → `/start_call_interview` endpoint

**Frequency:** Once per interview (at the start)

**Request Details:**
- **System Prompt:** Professional interviewer instructions
- **User Prompt:** Personalized greeting with candidate name and resume context
- **Response Format:** Plain text (conversational greeting)

**Estimated Token Usage:**
- Input: ~500-800 tokens
- Output: ~50-100 tokens
- **Total:** ~550-900 tokens per interview start

---

### 3. **Performance Summary Generation** 📊
**File:** `backend/src/interview_engine.py` → `generate_performance_summary()`  
**Uses:** `PERFORMANCE_SUMMARY_PROMPT` from `prompts.py`

**Frequency:** Once per interview (at the end, after 15 minutes of Q&A)

**Request Details:**
- **Prompt Includes:**
  - Full interview transcript (all questions and answers)
  - Performance metrics (average scores, confidence, question count)
  - Interview mode, job role, company
  - Duration information
- **Response Format:** Plain text (5-minute verbal summary)
- **Summary Covers:**
  - Overall impression
  - 3-5 key strengths with examples
  - 3-5 areas for improvement
  - Performance scores breakdown
  - 3-4 actionable recommendations
  - Motivational closing

**Estimated Token Usage:**
- Input: ~3,000-5,000 tokens (full transcript + context)
- Output: ~300-500 tokens (300-400 word summary)
- **Total:** ~3,300-5,500 tokens per interview completion

---

### 4. **Resume Analysis** 📄
**File:** `backend/src/grok_client.py` → `generate_resume_analysis()`  
**Called by:** `backend/src/resume_analyzer.py` → `analyze_resume_content()`

**Frequency:** Once per resume upload (when user clicks "Analyze Now")

**Request Details:**
- **Prompt:** `DETAILED_RESUME_ANALYSIS_PROMPT` (comprehensive career coach analysis)
- **Input:** Resume text (up to 15,000 characters)
- **Response Format:** JSON with detailed analysis
  ```json
  {
    "overall_score": 0-100,
    "summary": "Executive summary",
    "factor_scores": {
      "impact": 0-100,
      "skills": 0-100,
      "formatting": 0-100,
      "brevity": 0-100
    },
    "strengths": ["strength 1", "strength 2", ...],
    "weaknesses": ["weakness 1", "weakness 2", ...],
    "career_roadmap": ["step 1", "step 2", ...],
    "section_feedback": [...]
  }
  ```

**Estimated Token Usage:**
- Input: ~4,000-6,000 tokens (resume text + detailed prompt)
- Output: ~500-800 tokens (comprehensive analysis)
- **Total:** ~4,500-6,800 tokens per resume analysis

---

### 5. **Resume Recreation/Optimization** ✨
**File:** `backend/src/grok_client.py` → `generate_resume_analysis()` (reused)  
**Uses:** `RESUME_RECREATION_PROMPT` from `prompts.py`

**Frequency:** Once per resume optimization request

**Request Details:**
- **Prompt:** Extremely detailed ATS optimization instructions (longest prompt in the system)
- **Input:** 
  - Original resume text
  - Current ATS score
  - Target score
  - Specific improvement areas
- **Response Format:** JSON with optimized resume
  ```json
  {
    "resume_markdown": "Complete optimized resume",
    "new_score": 0-100,
    "improvements_made": [...],
    "keywords_added": [...],
    "content_expansion_ratio": "+25%",
    "quality_confidence": 0-100
  }
  ```

**Estimated Token Usage:**
- Input: ~6,000-8,000 tokens (massive prompt + resume)
- Output: ~2,000-3,500 tokens (full optimized resume in markdown)
- **Total:** ~8,000-11,500 tokens per resume recreation

---

### 6. **Mistake Detection & Content Analysis** 🔍
**File:** `backend/src/mistake_detector.py` → Uses `generate_text_response()`

**Frequency:** Every candidate answer (10-12 times per interview)

**Request Details:**
- **Purpose:** Detect rambling, off-topic answers, content quality
- **Input:** Question + candidate's answer + audio duration
- **Response Format:** Plain text analysis

**Estimated Token Usage:**
- Input: ~300-500 tokens
- Output: ~50-100 tokens
- **Total:** ~350-600 tokens per answer analysis

**Total for Interview (10-12 questions):**
- **~3,500-7,200 tokens per interview session**

---

## Total Credit Consumption Per User Journey

### Scenario 1: Resume Analysis Only
1. Resume upload & analysis: **~4,500-6,800 tokens**

**Total:** ~5,000-7,000 tokens

---

### Scenario 2: Resume Analysis + Optimization
1. Resume analysis: **~4,500-6,800 tokens**
2. Resume recreation: **~8,000-11,500 tokens**

**Total:** ~12,500-18,300 tokens

---

### Scenario 3: Complete Interview Session (Most Common)
1. Interview greeting: **~550-900 tokens**
2. Question generation (12 questions): **~17,000-32,400 tokens**
3. Mistake detection (12 answers): **~3,500-7,200 tokens**
4. Performance summary: **~3,300-5,500 tokens**

**Total:** ~24,350-46,000 tokens per interview

---

### Scenario 4: Full Platform Usage (Resume + Interview)
1. Resume analysis: **~4,500-6,800 tokens**
2. Resume optimization: **~8,000-11,500 tokens**
3. Complete interview: **~24,350-46,000 tokens**

**Total:** ~36,850-64,300 tokens per complete user journey

---

## Groq API Pricing Reference

> **Note:** Groq pricing as of December 2024 (verify current rates at [groq.com](https://groq.com))

**llama-3.3-70b-versatile:**
- Input: ~$0.59 per million tokens
- Output: ~$0.79 per million tokens

### Cost Estimates

**Per Complete Interview Session:**
- Input tokens: ~20,000-35,000 → **~$0.012-$0.021**
- Output tokens: ~4,000-8,000 → **~$0.003-$0.006**
- **Total cost per interview:** ~$0.015-$0.027 (1.5-2.7 cents)

**Per Complete User Journey (Resume + Interview):**
- Input tokens: ~30,000-50,000 → **~$0.018-$0.030**
- Output tokens: ~6,000-12,000 → **~$0.005-$0.009**
- **Total cost per user:** ~$0.023-$0.039 (2.3-3.9 cents)

---

## Rate Limiting & Error Handling

### Current Implementation
- **Rate Limit Detection:** System detects `rate_limit` errors in API responses
- **Fallback Behavior:**
  - Interview questions: Falls back to mock questions from `question_packs.py`
  - Resume analysis: Returns default scores with error message
- **Error Messages:** User-friendly notifications about API limits

### Recommendations
1. Implement exponential backoff for rate limit errors
2. Add request queuing for high-traffic scenarios
3. Monitor daily/monthly token usage
4. Set up alerts for approaching quota limits

---

## Optimization Opportunities

### 1. **Reduce Token Usage**
- ✅ Limit conversation history to last 6 exchanges (already implemented)
- ✅ Truncate resume text to 15,000 characters (already implemented)
- ⚠️ Consider caching resume analysis results
- ⚠️ Implement prompt compression techniques

### 2. **Batch Processing**
- Consider batching multiple resume analyses
- Pre-generate common interview questions

### 3. **Caching Strategy**
- Cache resume analysis for 24 hours (same resume, same results)
- Cache company-specific interview styles
- Store frequently used question templates

---

## Monitoring & Analytics

### Recommended Metrics to Track
1. **Total tokens consumed per day/month**
2. **Average tokens per interview session**
3. **API error rate and types**
4. **Response latency (p50, p95, p99)**
5. **Cost per user**
6. **Rate limit hit frequency**

### Implementation Suggestions
```python
# Add to grok_client.py
import time

def log_api_usage(endpoint, input_tokens, output_tokens, latency):
    """Log API usage for monitoring"""
    logger.info(f"API Usage - Endpoint: {endpoint}, "
                f"Input: {input_tokens}, Output: {output_tokens}, "
                f"Latency: {latency}ms, Cost: ${calculate_cost(input_tokens, output_tokens)}")
```

---

## Summary

### High-Level Token Breakdown
| Feature | Tokens per Use | Frequency | Total per User |
|---------|---------------|-----------|----------------|
| Interview Greeting | 550-900 | 1x | 550-900 |
| Question Generation | 1,700-2,700 | 10-12x | 17,000-32,400 |
| Mistake Detection | 350-600 | 10-12x | 3,500-7,200 |
| Performance Summary | 3,300-5,500 | 1x | 3,300-5,500 |
| Resume Analysis | 4,500-6,800 | 1x | 4,500-6,800 |
| Resume Optimization | 8,000-11,500 | 1x | 8,000-11,500 |

### Key Insights
- **Most expensive operation:** Resume optimization (~8,000-11,500 tokens)
- **Highest frequency:** Question generation (10-12x per interview)
- **Largest cumulative cost:** Interview Q&A cycle (~20,000-40,000 tokens)
- **Average cost per user:** 2-4 cents (extremely cost-effective)

---

## Conclusion

The AI interview system is **highly cost-efficient** with Groq's competitive pricing:
- **Per interview:** ~1.5-2.7 cents
- **Per complete user journey:** ~2.3-3.9 cents

This makes the platform scalable for high-volume usage while maintaining premium AI-powered features.

---

**Last Updated:** December 14, 2025  
**Model:** llama-3.3-70b-versatile  
**API Provider:** Groq
