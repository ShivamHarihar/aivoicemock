# Project Documentation: Sampro AI Interview Platform

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Core Features](#core-features)
4. [Directory Structure](#directory-structure)
5. [Backend Components](#backend-components)
6. [Frontend Components](#frontend-components)
7. [Recent Implementations](#recent-implementations)
8. [API Endpoints](#api-endpoints)
9. [Data Flow](#data-flow)
10. [Configuration & Setup](#configuration--setup)

---

## Project Overview

**Sampro AI Interview Platform** is a comprehensive AI-powered mock interview system that provides:
- **Real-time Voice Interviews** with AI interviewer
- **Performance Analysis** (pace, confidence, content quality)
- **ATS Resume Analyzer** with scoring
- **AI Resume Recreator** for ATS optimization
- **Timed Interview System** with automatic phase transitions
- **Multi-language Support** (English, Hindi, Marathi)

### Technology Stack
- **Backend**: Flask (Python 3.8+)
- **AI/LLM**: Groq API (llama-3.3-70b-versatile)
- **Speech-to-Text**: Browser Web Speech API + Whisper (fallback)
- **Text-to-Speech**: Edge TTS (neural voices)
- **NLP**: SpaCy
- **PDF Generation**: ReportLab
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                         │
│  (Browser: HTML/CSS/JS + Web Speech API + Audio Visualizer) │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                   FLASK WEB SERVER                          │
│              (app.py - Route Handlers)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼────┐ ┌──────▼────────┐
│ Interview    │ │ Resume  │ │ Memory Store  │
│ Engine       │ │ Analyzer│ │ (Sessions)    │
└───────┬──────┘ └────┬────┘ └───────────────┘
        │             │
┌───────▼─────────────▼──────────────────────────────┐
│           AI/LLM SERVICES                          │
│  • Groq API (Question Generation, Analysis)       │
│  • Edge TTS (Text-to-Speech)                      │
│  • Whisper (Speech-to-Text Fallback)             │
└────────────────────────────────────────────────────┘
```

---

## Core Features

### 1. AI Voice Interview System
- **Real-time Conversation**: Natural back-and-forth dialogue
- **Voice Activity Detection (VAD)**: Auto-detects speech start/end
- **Automatic Silence Detection**: 1.5s silence triggers processing
- **Barge-in Support**: User can interrupt AI
- **Multi-mode Interviews**: HR, Technical, Behavioral
- **Company-specific Styles**: Google, Amazon, Microsoft, etc.
- **Role-based Questions**: Tailored to job role

### 2. Timed Interview System (NEW)
- **4-Minute Quick Test Mode**: 2 min Q&A + 2 min Summary
- **20-Minute Production Mode**: 15 min Q&A + 5 min Summary
- **Visual Countdown Timer**: Shows time remaining and current phase
- **Auto-trigger Summary**: Automatically generates performance summary
- **Phase Transitions**: Smooth transition from Q&A to Summary
- **Progress Bar**: Visual progress indicator

### 3. Real-time Performance Analysis
- **Audio Analysis**:
  - Speaking pace (Words Per Minute)
  - Filler word detection ("um", "uh", "like")
  - Confidence scoring (0-100)
  - Pause detection
- **Content Analysis**:
  - Relevance checking
  - Rambling detection
  - STAR method structure analysis
  - Script reading detection
- **Live Feedback**: Tips displayed during interview

### 4. ATS Resume Analyzer
- **Multi-format Support**: PDF, TXT
- **Comprehensive Scoring**:
  - Overall ATS Score (0-100)
  - Keyword density
  - Format compliance
  - Content quality
- **Detailed Feedback**:
  - Strengths identification
  - Weaknesses analysis
  - Improvement suggestions

### 5. AI Resume Recreator
- **ATS Optimization**: Rewrites resume for higher ATS scores
- **Keyword Enhancement**: Adds relevant industry keywords
- **Format Standardization**: Ensures ATS-friendly formatting
- **Fact Preservation**: Maintains all original information
- **Multi-format Export**: PDF and Markdown

---

## Directory Structure

```
sampro-ai-interview/
├── backend/
│   ├── app/
│   │   └── app.py                 # Flask application entry point
│   └── src/
│       ├── interview_engine.py    # Interview state management
│       ├── audio_analyzer.py      # Speech analysis
│       ├── mistake_detector.py    # Content quality analysis
│       ├── scoring.py             # Performance scoring
│       ├── resume_analyzer.py     # Resume parsing & analysis
│       ├── resume_recreator.py    # AI resume rewriting
│       ├── pdf_generator.py       # PDF generation
│       ├── groq_client.py         # Groq API wrapper
│       ├── edge_tts_client.py     # Text-to-Speech
│       ├── whisper_stt.py         # Speech-to-Text
│       ├── memory_store.py        # Session management
│       ├── prompts.py             # LLM prompts
│       ├── question_packs.py      # Interview questions
│       ├── spacy_parser.py        # NLP parsing
│       └── utils.py               # Utilities
├── frontend/
│   ├── src/
│   │   ├── base.html              # Base template
│   │   ├── index.html             # Landing page
│   │   ├── dashboard.html         # Interview dashboard
│   │   ├── interview.html         # Interview interface
│   │   ├── result.html            # Results page
│   │   ├── resume_analysis.html   # Resume upload
│   │   └── ats_dashboard.html     # Resume dashboard
│   └── public/
│       ├── js/
│       │   ├── script.js          # Interview logic
│       │   └── ats_dashboard.js   # Resume dashboard logic
│       └── css/
│           └── style.css          # Global styles
├── scripts/
│   ├── verify_system.py           # System diagnostics
│   ├── test_system.py             # Integration tests
│   └── quick_test_interview.py    # Quick test script
├── configs/
│   ├── requirements.txt           # Python dependencies
│   └── timing_config.py           # Timing configurations
└── Documentation/
    ├── PROJECT_DOCUMENTATION.md   # This file
    ├── PROJECT_FLOW_END_TO_END.txt
    ├── QUICK_REFERENCE_FLOW.txt
    ├── FEATURES_SUMMARY.txt
    ├── README_DOCUMENTATION_INDEX.txt
    ├── QUICK_TEST_MODE_README.md
    ├── AUTO_SUMMARY_FIX.md
    ├── COUNTDOWN_TIMER_ADDED.md
    └── 500_ERROR_FIX.md
```

---

## Backend Components

### 1. `app.py` - Flask Application
**Purpose**: Main web server and API endpoint definitions

**Key Routes**:
- `GET /` - Landing page
- `GET /dashboard` - Interview dashboard
- `GET /interview` - Interview interface
- `POST /start_call_interview` - Initialize interview session
- `POST /process_voice` - Process user answer
- `POST /upload_profile` - Upload resume for context
- `POST /final_results` - Get interview results
- `POST /api/analyze_resume` - Analyze resume
- `POST /api/recreate_resume` - Recreate resume with AI
- `POST /api/download_resume_pdf` - Download PDF resume

**Functions**:
```python
def start_call_interview():
    # Creates session, generates greeting
    # Returns: session_id, audio_url, message

def process_voice():
    # Main interview loop
    # Receives: user_text or audio file
    # Returns: AI response with audio

def final_results():
    # Calculates final scores
    # Returns: scorecard with metrics
```

### 2. `interview_engine.py` - Interview State Management
**Purpose**: Orchestrates interview flow and phase management

**Classes**:
```python
class InterviewEngine:
    def check_interview_phase(session):
        # Checks if Q&A or Summary phase
        # Returns: ('qa'|'summary', elapsed_seconds)
    
    def generate_performance_summary(session_id, elapsed_seconds):
        # Generates comprehensive performance summary
        # Returns: {full_text, phase, interview_complete}
    
    def process_answer(session_id, user_audio_text, audio_duration):
        # Main processing pipeline:
        # 1. Check for auto-summary trigger
        # 2. Analyze audio (pace, confidence)
        # 3. Detect mistakes (relevance, rambling)
        # 4. Calculate scores
        # 5. Generate AI response
        # 6. Update session memory
        # Returns: {full_text, difficulty, real_time_feedback}
```

**Timing Constants**:
```python
INTERVIEW_DURATION_MINUTES = 4  # Total: 4 minutes
QA_PHASE_MINUTES = 2            # Q&A: 2 minutes
# Summary phase: 2 minutes (auto-calculated)
```

### 3. `audio_analyzer.py` - Speech Analysis
**Purpose**: Analyzes linguistic characteristics of answers

**Classes**:
```python
class AudioAnalyzer:
    def analyze_text(text, duration_seconds):
        # Analyzes: WPM, fillers, confidence
        # Returns: {
        #   confidence_score, confidence_level,
        #   speaking_pace, pace_category,
        #   filler_count, tips, issues
        # }
    
    def _calculate_confidence(...):
        # Heuristic confidence scoring (0-100)
        # Factors: fillers, pace, length
    
    def detect_script_reading(text):
        # Detects overly formal/scripted answers
```

### 4. `mistake_detector.py` - Content Quality Analysis
**Purpose**: Identifies content-related issues

**Classes**:
```python
class MistakeDetector:
    def detect_rambling(text):
        # Checks for excessive length/repetition
    
    def check_relevance(question, answer):
        # Uses LLM to verify answer relevance
    
    def analyze_structure(text):
        # Checks for STAR method components
    
    def detect_all_mistakes(...):
        # Aggregates all checks
        # Returns: {all_feedback, has_issues}
```

### 5. `scoring.py` - Performance Scoring
**Purpose**: Quantitative evaluation

**Functions**:
```python
def calculate_local_metrics(text, audio_duration):
    # Deterministic scoring without LLM
    # Factors: clarity, fluency, pace
    # Returns: score (0-10)

def get_semantic_score(mode, resume_summary, transcript):
    # LLM-based qualitative evaluation
    # Returns: {technical_depth, communication, ...}

def calculate_final_score(semantic_score_data, local_score):
    # Weighted average of AI and local scores
    # Returns: final_score (0-10)
```

### 6. `groq_client.py` - LLM API Wrapper
**Purpose**: Interface to Groq API

**Functions**:
```python
def generate_response(prompt):
    # Sends prompt, expects JSON response
    # Model: llama-3.3-70b-versatile
    # Returns: {reaction, follow_up_question, score, feedback}
```

### 7. `edge_tts_client.py` - Text-to-Speech
**Purpose**: Converts text to speech audio

**Functions**:
```python
def generate_audio_sync(text, output_path):
    # Generates audio file
    # Voice: en-US-AriaNeural

def generate_audio_memory_sync(text):
    # Generates audio in memory (faster)
    # Returns: audio bytes
```

### 8. `memory_store.py` - Session Management
**Purpose**: In-memory session storage

**Data Structure**:
```python
sessions = {
    'session_id': {
        'mode': 'Technical',
        'job_role': 'Software Engineer',
        'company': 'Google',
        'start_time': datetime,
        'interview_phase': 'qa'|'summary'|'completed',
        'history': [
            {'role': 'ai', 'content': '...'},
            {'role': 'user', 'content': '...'}
        ],
        'scores': [
            {'local_score': 7.5, 'ai_score': 8.0, ...}
        ],
        'analyses': [
            {'audio': {...}, 'mistakes': {...}}
        ]
    }
}
```

### 9. `prompts.py` - LLM Prompts
**Purpose**: Stores system prompts and templates

**Key Prompts**:
- `SYSTEM_INSTRUCTION`: Base AI personality
- `FOLLOW_UP_PROMPT_TEMPLATE`: Question generation
- `PERFORMANCE_SUMMARY_PROMPT`: Summary generation
- `SCORING_PROMPT_TEMPLATE`: Final scoring
- `RESUME_RECREATION_PROMPT`: Resume rewriting

### 10. `question_packs.py` - Interview Questions
**Purpose**: Static question database

**Data**:
```python
JOB_ROLE_QUESTIONS = {
    'Software Engineer': [...],
    'Data Scientist': [...],
    'Product Manager': [...]
}

COMPANY_STYLES = {
    'Google': 'Focus on problem-solving...',
    'Amazon': 'Use leadership principles...'
}
```

---

## Frontend Components

### 1. `script.js` - Interview Interface Logic
**Purpose**: Manages interview UI and real-time interaction

**Key Variables**:
```javascript
// Timer and summary trigger
let interviewStartTime = null;
let summaryTriggered = false;
const QA_PHASE_DURATION = 2 * 60 * 1000; // 2 minutes

// Speech recognition
let recognition; // Web Speech API
let lastTranscript = '';
let speechEndTimer;

// Audio
let currentAudio = null;
let isProcessing = false;
```

**Key Functions**:
```javascript
function startInterview():
    // Collects inputs, initiates session

function playGreeting(audioUrl, text):
    // Plays AI greeting, starts timer

function startSummaryCheck():
    // Checks elapsed time every second
    // Triggers summary at 2:00 mark

function updateTimerDisplay(elapsedSeconds, ...):
    // Updates countdown timer UI
    // Shows phase, time remaining, progress

function triggerSummary():
    // Stops listening
    // Sends [AUTO_SUMMARY_TRIGGER] to backend
    // Plays summary response

function startRecording():
    // Starts Web Speech API
    // Handles speech recognition events

function sendText(text):
    // Sends user answer to backend
    // Receives AI response

function playResponse(audioData, text, isSummary):
    // Plays AI audio
    // If summary: redirects to results
    // If Q&A: restarts listening
```

### 2. `interview.html` - Interview Interface
**Purpose**: UI for active interview

**Key Elements**:
```html
<!-- Status Display -->
<h2 id="status">Initializing...</h2>

<!-- Countdown Timer -->
<div id="timer-container">
    <div class="timer-phase" id="timer-phase">Q&A Phase</div>
    <div class="timer-time" id="timer-time">2:00</div>
    <div class="timer-progress-fill" id="timer-progress"></div>
</div>

<!-- Audio Visualizer -->
<div class="visualizer-container">
    <div class="visualizer-circle"></div>
</div>

<!-- Controls -->
<button onclick="stopRecording()">✓ Force Send</button>
<button onclick="endInterview()">End Session</button>
```

**Timer Styles**:
- Q&A Phase: Green (#10b981)
- Summary Phase: Orange (#f59e0b)
- Warning (< 60s): Pulsing orange
- Critical (< 30s): Pulsing red

---

## Recent Implementations

### 1. Auto-Summary Trigger System (December 2025)
**Problem**: Summary phase wasn't automatically generating at 2-minute mark

**Solution**:
- Added timer tracking in frontend (`interviewStartTime`)
- Created `startSummaryCheck()` interval (checks every second)
- Auto-sends `[AUTO_SUMMARY_TRIGGER]` at 2:00
- Backend detects trigger and generates summary
- Frontend stops listening and plays summary
- Redirects to results after summary

**Files Modified**:
- `frontend/public/js/script.js`: Added timer logic
- `backend/src/interview_engine.py`: Added trigger detection

### 2. Countdown Timer Display (December 2025)
**Features**:
- Visual countdown showing time remaining
- Phase indicator (Q&A / Summary)
- Progress bar
- Color-coded warnings
- Smooth animations

**Files Modified**:
- `frontend/src/interview.html`: Added timer HTML/CSS
- `frontend/public/js/script.js`: Added `updateTimerDisplay()`

### 3. 4-Minute Quick Test Mode (December 2025)
**Purpose**: Faster testing during development

**Configuration**:
```python
# backend/src/interview_engine.py
INTERVIEW_DURATION_MINUTES = 4  # Total: 4 minutes
QA_PHASE_MINUTES = 2            # Q&A: 2 minutes
```

**Modes Available**:
- Quick Test: 4 min (2 min Q&A + 2 min Summary)
- Standard Test: 10 min (7 min Q&A + 3 min Summary)
- Production: 20 min (15 min Q&A + 5 min Summary)

---

## API Endpoints

### Interview Endpoints

#### `POST /start_call_interview`
**Request**:
```json
{
  "mode": "Technical",
  "job_role": "Software Engineer",
  "company": "Google"
}
```

**Response**:
```json
{
  "session_id": "abc123",
  "audio_url": "/serve_audio/greeting.mp3",
  "message": "Hello! Welcome to your technical interview..."
}
```

#### `POST /process_voice`
**Request**:
```json
{
  "session_id": "abc123",
  "user_text": "I have 5 years of experience in Python..."
}
```

**Response**:
```json
{
  "user_text": "I have 5 years...",
  "full_text": "That's great! Can you tell me about a challenging project?",
  "audio_base64": "base64_encoded_audio",
  "difficulty": "Normal",
  "phase": "qa",
  "elapsed_seconds": 45,
  "interview_complete": false,
  "real_time_feedback": {
    "confidence": "High",
    "pace": "Optimal",
    "filler_count": 2,
    "tips": ["Great pace!", "Reduce filler words"],
    "issues": []
  }
}
```

#### `POST /final_results`
**Request**:
```json
{
  "session_id": "abc123"
}
```

**Response**:
```json
{
  "final_score": 8.5,
  "local_score": 8.0,
  "ai_score": 9.0,
  "avg_confidence": 85,
  "total_questions": 5,
  "feedback": "Strong performance overall..."
}
```

### Resume Endpoints

#### `POST /api/analyze_resume`
**Request**: FormData with resume file

**Response**:
```json
{
  "ats_score": 75,
  "strengths": ["Clear formatting", "Relevant keywords"],
  "weaknesses": ["Missing metrics", "Too long"],
  "suggestions": ["Add quantifiable achievements"]
}
```

#### `POST /api/recreate_resume`
**Request**:
```json
{
  "resume_text": "Original resume...",
  "current_score": 75,
  "analysis_data": {...}
}
```

**Response**:
```json
{
  "recreated_resume": "# John Doe\n## Experience\n...",
  "improvements": ["Added keywords", "Improved formatting"]
}
```

---

## Data Flow

### Interview Flow
```
1. User starts interview
   ↓
2. Frontend: startInterview()
   → POST /start_call_interview
   ↓
3. Backend: Creates session, generates greeting
   → Returns session_id + greeting audio
   ↓
4. Frontend: Plays greeting, starts timer, starts listening
   ↓
5. User speaks → Web Speech API transcribes
   ↓
6. Frontend: sendText(transcript)
   → POST /process_voice
   ↓
7. Backend: 
   - Checks interview phase
   - Analyzes answer (audio + content)
   - Calculates scores
   - Generates AI response
   - Converts to speech
   → Returns AI response + audio
   ↓
8. Frontend: Plays AI audio, restarts listening
   ↓
9. Repeat steps 5-8 until 2:00 mark
   ↓
10. At 2:00: Frontend triggers summary
    → POST /process_voice with [AUTO_SUMMARY_TRIGGER]
    ↓
11. Backend: Generates performance summary
    → Returns summary + audio
    ↓
12. Frontend: Plays summary, redirects to results
```

### Timer Flow
```
Interview starts
  ↓
interviewStartTime = Date.now()
startSummaryCheck() // Interval every 1 second
  ↓
Every second:
  - Calculate elapsed time
  - Update timer display (MM:SS)
  - Update progress bar
  - Check if >= 2 minutes
  ↓
At 2:00:
  - summaryTriggered = true
  - Stop listening
  - Send [AUTO_SUMMARY_TRIGGER]
  - Play summary
  - Redirect to results
```

---

## Configuration & Setup

### Environment Variables
```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Python Dependencies
```
flask==2.3.0
groq==0.4.0
edge-tts==6.1.9
openai-whisper==20230918
spacy==3.7.2
reportlab==4.0.7
PyPDF2==3.0.1
python-dotenv==1.0.0
```

### Installation
```bash
# 1. Clone repository
git clone <repo-url>
cd sampro-ai-interview

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r configs/requirements.txt

# 4. Download SpaCy model
python -m spacy download en_core_web_sm

# 5. Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 6. Run application
cd backend/app
python app.py
```

### Running the Application
```bash
# Development server
cd backend/app
python app.py

# Access at: http://localhost:5000
```

### Testing
```bash
# Quick test (4-minute interview)
python scripts/quick_test_interview.py

# System verification
python scripts/verify_system.py

# Integration tests
python scripts/test_system.py
```

---

## Performance Metrics

### Interview Scoring
- **Local Score** (0-10): Deterministic metrics
  - Clarity: Word count, sentence structure
  - Fluency: Speaking pace, pauses
  - Pace: WPM (optimal: 120-160)
  
- **AI Score** (0-10): LLM evaluation
  - Technical depth
  - Communication quality
  - Relevance to question
  
- **Final Score**: Weighted average
  - 40% Local Score
  - 60% AI Score

### Real-time Feedback
- **Confidence Score** (0-100):
  - Base: 70
  - Filler words: -5 per filler
  - Pace: +10 optimal, -10 too fast/slow
  - Length: +5 good length

- **Speaking Pace Categories**:
  - Too Slow: < 100 WPM
  - Optimal: 120-160 WPM
  - Too Fast: > 180 WPM

---

## Troubleshooting

### Common Issues

**1. Microphone not working**
- Check browser permissions
- Use HTTPS or localhost
- Try different browser (Chrome recommended)

**2. Summary not generating**
- Check browser console for errors
- Verify GROQ_API_KEY is set
- Check backend logs for errors

**3. Timer not showing**
- Hard refresh browser (Ctrl+F5)
- Check timer-container display style
- Verify JavaScript loaded

**4. Audio not playing**
- Check Edge TTS installation
- Verify audio file generation
- Check browser audio permissions

---

## Future Enhancements

### Planned Features
- [ ] Multi-language interview support
- [ ] Video interview capability
- [ ] Interview recording/playback
- [ ] Advanced analytics dashboard
- [ ] Interview history tracking
- [ ] Custom question banks
- [ ] Team collaboration features
- [ ] Mobile app version

### Technical Improvements
- [ ] WebSocket for real-time communication
- [ ] Database integration (PostgreSQL)
- [ ] Redis for session management
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit test coverage
- [ ] Performance optimization
- [ ] Security hardening

---

## Contributing

### Code Style
- Python: PEP 8
- JavaScript: ES6+
- HTML/CSS: BEM methodology

### Git Workflow
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## License

Proprietary - Sampro Ltd.

---

## Contact & Support

For questions or support:
- Email: support@sampro.ai
- Documentation: See README_DOCUMENTATION_INDEX.txt
- Issues: GitHub Issues

---

**Last Updated**: December 1, 2025
**Version**: 2.0.0
**Status**: Production Ready
