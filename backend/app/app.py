import sys
import os

# Add the project root to sys.path to allow imports from backend.src
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

from backend.src.utils import generate_session_id, ensure_directory, logger, get_timestamp
from backend.src.memory_store import memory
from backend.src.interview_engine import engine
from backend.src.whisper_stt import transcribe_audio
from backend.src.edge_tts_client import generate_audio_sync
from backend.src.spacy_parser import parse_resume
from backend.src.scoring import get_semantic_score, calculate_final_score
import backend.src.resume_analyzer as resume_analyzer
import backend.src.resume_recreator as resume_recreator
import backend.src.pdf_generator as pdf_generator
from backend.src.template_registry import registry

# Define paths relative to this file (backend/app/app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', '..', 'frontend')
STATIC_FOLDER = os.path.join(FRONTEND_DIR, 'public')
TEMPLATE_FOLDER = os.path.join(FRONTEND_DIR, 'src')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
AUDIO_FOLDER = os.path.join(STATIC_FOLDER, 'audio')
ensure_directory(UPLOAD_FOLDER)
ensure_directory(AUDIO_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/resume_analysis')
def resume_analysis():
    return render_template('resume_analysis.html')

@app.route('/analysis_loading')
def analysis_loading():
    return render_template('analysis_loading.html')

@app.route('/ats_dashboard')
def ats_dashboard():
    return render_template('ats_dashboard.html')

@app.route('/recreate_resume_page')
def recreate_resume_page():
    return render_template('recreate_resume.html')

@app.route('/create-resume')
def create_resume():
    return render_template('create_resume.html')

@app.route('/resume/builder')
def resume_builder():
    template_id = request.args.get('template', 'modern')
    return render_template('resume_builder.html', template_id=template_id)

@app.route('/resume_view')
def resume_view():
    return render_template('resume_view.html')

@app.route('/template_card_preview/<template_id>')
def template_card_preview(template_id):
    return render_template('template_card_preview.html', template_id=template_id)

@app.route('/api/templates', methods=['GET'])
def get_templates():
    category = request.args.get('category')
    if category and category != 'all':
        templates = registry.get_templates_by_category(category)
    else:
        templates = registry.get_all_templates()
    return jsonify({"templates": templates})

@app.route('/api/analyze_resume', methods=['POST'])
def api_analyze_resume():
    try:
        if 'resume' not in request.files:
            logger.error("No resume file in request")
            return jsonify({"error": "No resume file provided"}), 400
            
        resume_file = request.files['resume']
        if resume_file.filename == '':
            logger.error("Empty filename")
            return jsonify({"error": "No selected file"}), 400
            
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(filepath)
        
        logger.info(f"Resume file saved: {filename}")
        
        # Parse text
        text_content = resume_analyzer.parse_resume(filepath)
        if not text_content:
            logger.error("Failed to parse resume")
            return jsonify({"error": "Could not parse resume file. Please try a different PDF or TXT file."}), 400

        logger.info(f"Resume parsed, length: {len(text_content)} characters")
        
        # Analyze with Grok
        analysis_result = resume_analyzer.analyze_resume_content(text_content)
        
        logger.info(f"Analysis result: {analysis_result}")
        
        if "error" in analysis_result:
            logger.error(f"Analysis error: {analysis_result['error']}")
            return jsonify(analysis_result), 400
        
        # Add original filename and file URL to result
        original_name = os.path.splitext(filename)[0]
        analysis_result['original_filename'] = original_name
        analysis_result['file_url'] = f'/static/uploads/{filename}'
        analysis_result['file_type'] = 'pdf' if filename.lower().endswith('.pdf') else 'txt'
             
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Error in resume analysis API: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/recreate_resume', methods=['POST'])
def api_recreate_resume():
    try:
        data = request.json
        logger.info(f"Received recreation request with data keys: {data.keys() if data else 'None'}")
        
        resume_text = data.get('resume_text', '') if data else ''
        current_score = data.get('current_score', 70) if data else 70
        analysis = data.get('analysis', {}) if data else {}
        
        logger.info(f"Resume text length: {len(resume_text)}")
        logger.info(f"Current score: {current_score}")
        
        if not resume_text:
            logger.warning("No resume text provided in request")
            return jsonify({"error": "No resume text provided. Please upload and analyze a resume first."}), 400
        
        logger.info("Starting AI resume recreation...")
        
        # Call recreation function
        result = resume_recreator.recreate_resume_with_ai(
            resume_text=resume_text,
            current_score=current_score,
            analysis_data=analysis
        )
        
        if "error" in result:
            logger.error(f"Recreation error: {result['error']}")
            return jsonify(result), 400
        
        logger.info("Resume recreation successful")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in resume recreation API: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/download_resume_pdf', methods=['POST'])
def api_download_resume_pdf():
    """Generate and download resume as PDF"""
    try:
        logger.info("PDF download request received")
        
        # Check if request has JSON data
        if not request.json:
            logger.error("No JSON data in request")
            return jsonify({"error": "No data provided"}), 400
        
        data = request.json
        logger.info(f"Request data keys: {list(data.keys())}")
        
        markdown_text = data.get('markdown_text', '')
        template_id = data.get('template_id', 'modern')  # Default to 'modern' template
        
        if not markdown_text:
            logger.error("No markdown text provided")
            return jsonify({"error": "No resume content provided"}), 400
        
        # Validate template_id
        allowed_templates = [
            'classic', 'modern', 'creative', 'professional', 'minimal',
            'template-1', 'template-2', 'template-3', 'template-4', 'template-5',
            'template-6', 'template-7', 'template-8', 'template-9', 'template-10',
            'template-11', 'template-12', 'template-13', 'template-14', 'template-15'
        ]
        if template_id not in allowed_templates:
            logger.warning(f"Invalid template_id '{template_id}', defaulting to 'modern'")
            template_id = 'modern'
        
        logger.info(f"Generating PDF with template '{template_id}' (length: {len(markdown_text)} chars)...")
        logger.info(f"First 100 chars: {markdown_text[:100]}")
        
        try:
            # Try template-based PDF generation
            logger.info(f"Attempting template-based PDF generation with '{template_id}' template...")
            pdf_bytes = pdf_generator.markdown_to_pdf(markdown_text, template_id=template_id)
            logger.info(f"✅ PDF generated successfully, size: {len(pdf_bytes)} bytes")
        except Exception as pdf_error:
            logger.error(f"Fancy PDF generation failed: {pdf_error}", exc_info=True)
            # Fallback to simple PDF
            logger.info("Attempting fallback simple PDF generation...")
            try:
                pdf_bytes = generate_simple_pdf(markdown_text)
                logger.info(f"✅ Simple PDF generated, size: {len(pdf_bytes)} bytes")
            except Exception as fallback_error:
                logger.error(f"Simple PDF also failed: {fallback_error}", exc_info=True)
                # Emergency fallback - super minimal PDF
                logger.info("Attempting emergency minimal PDF...")
                try:
                    pdf_bytes = generate_emergency_pdf(markdown_text)
                    logger.info(f"✅ Emergency PDF generated, size: {len(pdf_bytes)} bytes")
                except Exception as emergency_error:
                    logger.error(f"All PDF generation methods failed: {emergency_error}", exc_info=True)
                    return jsonify({"error": f"PDF generation failed: {str(emergency_error)}"}), 500
        
        # Send PDF as downloadable file
        from flask import send_file
        import io
        
        logger.info("Creating PDF buffer for download...")
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        logger.info("Sending PDF file...")
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'optimized_resume_{template_id}.pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

@app.route('/api/generate_preview_pdf', methods=['POST'])
def api_generate_preview_pdf():
    """Generate resume PDF for preview (inline)"""
    try:
        if not request.json:
            return jsonify({"error": "No data provided"}), 400
        
        data = request.json
        markdown_text = data.get('markdown_text', '')
        template_id = data.get('template_id', 'modern')
        
        if not markdown_text:
            return jsonify({"error": "No resume content provided"}), 400
        
        # Consistent template validation
        allowed_templates = [
            'classic', 'modern', 'creative', 'professional', 'minimal',
            'template-1', 'template-2', 'template-3', 'template-4', 'template-5',
            'template-6', 'template-7', 'template-8', 'template-9', 'template-10',
            'template-11', 'template-12', 'template-13', 'template-14', 'template-15'
        ]
        if template_id not in allowed_templates:
            template_id = 'modern'
            
        # Generate PDF bytes (reusing logic or calling generator directly)
        try:
            pdf_bytes = pdf_generator.markdown_to_pdf(markdown_text, template_id=template_id)
        except Exception:
            try:
                pdf_bytes = generate_simple_pdf(markdown_text)
            except Exception:
                pdf_bytes = generate_emergency_pdf(markdown_text)

        # Send PDF inline
        from flask import send_file
        import io
        
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False, # Inline for preview
            download_name=f'preview_{template_id}.pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating preview PDF: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/download_resume_docx', methods=['POST'])
def api_download_resume_docx():
    """Generate and download resume as DOCX"""
    try:
        logger.info("DOCX download request received")
        
        if not request.json:
            return jsonify({"error": "No data provided"}), 400
        
        data = request.json
        markdown_text = data.get('markdown_text', '')
        template_id = data.get('template_id', 'modern')
        
        if not markdown_text:
            return jsonify({"error": "No resume content provided"}), 400
            
        # Import here to avoid circular imports or startup errors if missing
        from backend.src.docx_generator import markdown_to_docx
        
        docx_bytes = markdown_to_docx(markdown_text, template_id)
        
        # Send DOCX as downloadable file
        from flask import send_file
        import io
        
        docx_buffer = io.BytesIO(docx_bytes)
        docx_buffer.seek(0)
        
        return send_file(
            docx_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'optimized_resume_{template_id}.docx'
        )
        
    except Exception as e:
        logger.error(f"Error generating DOCX: {e}", exc_info=True)
        return jsonify({"error": f"Failed to generate DOCX: {str(e)}"}), 500

def generate_simple_pdf(markdown_text):
    """Fallback simple PDF generator using reportlab basics"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        
        logger.info("Starting simple PDF generation...")
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Simple text rendering
        y = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Optimized Resume")
        
        y -= 30
        c.setFont("Helvetica", 10)
        
        # Split text into lines
        lines = markdown_text.split('\n')
        logger.info(f"Processing {len(lines)} lines...")
        
        for i, line in enumerate(lines):
            if y < 50:  # New page if needed
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            
            # Remove markdown formatting for simple display
            clean_line = line.replace('#', '').replace('**', '').replace('*', '').strip()
            
            # Handle special characters that might cause issues
            clean_line = clean_line.encode('ascii', 'ignore').decode('ascii')
            
            if clean_line:
                # Wrap long lines
                if len(clean_line) > 90:
                    words = clean_line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 90:
                            current_line += word + " "
                        else:
                            if current_line.strip():
                                c.drawString(50, y, current_line.strip())
                                y -= 15
                            current_line = word + " "
                    if current_line.strip():
                        c.drawString(50, y, current_line.strip())
                        y -= 15
                else:
                    c.drawString(50, y, clean_line)
                    y -= 15
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Simple PDF generated successfully: {len(pdf_bytes)} bytes")
        return pdf_bytes
        
    except Exception as e:
        logger.error(f"Simple PDF generation error: {e}", exc_info=True)
        raise

def generate_emergency_pdf(markdown_text):
    """Emergency ultra-simple PDF generator - guaranteed to work"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        
        logger.info("Creating emergency minimal PDF...")
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Ultra simple - just dump text
        y = 750
        c.setFont("Helvetica", 10)
        
        # Strip all special characters and just use plain text
        plain_text = markdown_text.replace('#', '').replace('*', '').replace('_', '')
        plain_text = plain_text.encode('ascii', 'ignore').decode('ascii')
        
        for line in plain_text.split('\n')[:100]:  # Limit to 100 lines
            if y < 50:
                break
            if line.strip():
                # Truncate long lines
                safe_line = line[:100].strip()
                if safe_line:
                    try:
                        c.drawString(50, y, safe_line)
                    except:
                        c.drawString(50, y, "...")
                    y -= 12
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Emergency PDF created: {len(pdf_bytes)} bytes")
        return pdf_bytes
        
    except Exception as e:
        logger.error(f"Emergency PDF failed: {e}", exc_info=True)
        raise

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/interview')
def interview():
    """Renders the interview page."""
    session_id = request.args.get('session_id', '')
    return render_template('interview.html', session_id=session_id)

@app.route('/result')
def result():
    """Renders the results page."""
    session_id = request.args.get('session_id', '')
    return render_template('result.html', session_id=session_id)



@app.route('/start_call_interview', methods=['POST'])
def start_call_interview():
    """Initializes a new interview session."""
    try:
        data = request.json
        mode = data.get('mode', 'HR')
        job_role = data.get('job_role', '')
        company = data.get('company', '')
        resume_text = data.get('resume_text', '')  # Resume text from frontend
        
        session_id = generate_session_id()
        
        memory.create_session(session_id)
        memory.update_session(session_id, 'mode', mode)
        
        # Store job role and company in session
        if job_role:
            memory.update_session(session_id, 'job_role', job_role)
        if company:
            memory.update_session(session_id, 'company', company)
        
        # Parse resume if provided
        candidate_name = None
        if resume_text and len(resume_text.strip()) > 50:
            from backend.src.resume_parser import extract_candidate_info
            
            logger.info(f"Parsing resume (length: {len(resume_text)} chars)")
            resume_context = extract_candidate_info(resume_text)
            
            # Store resume context in session
            memory.update_session(session_id, 'resume_context', resume_context)
            memory.update_session(session_id, 'candidate_name', resume_context.get('candidate_name'))
            memory.update_session(session_id, 'resume_topics', resume_context.get('topics', []))
            
            # Initialize topic question count
            topic_count = {}
            for topic in resume_context.get('topics', []):
                topic_count[topic] = 0
            memory.update_session(session_id, 'topic_question_count', topic_count)
            
            candidate_name = resume_context.get('candidate_name')
            logger.info(f"Resume parsed: Name={candidate_name}, Topics={len(resume_context.get('topics', []))}")
        
        # Generate welcoming greeting with context
        greeting_context = ""
        if job_role:
            greeting_context += f" for the {job_role} position"
        if company:
            greeting_context += f" at {company}"
        
        # Personalize greeting with candidate name if available
        if candidate_name:
            initial_greeting = f"Hello {candidate_name}! I'm your AI interviewer. Welcome to your {mode} interview{greeting_context}. I'm excited to learn more about you. To begin, please introduce yourself."
        else:
            initial_greeting = f"Hello! I'm your AI interviewer. Welcome to your {mode} interview{greeting_context}. I'm excited to learn more about you. To begin, please introduce yourself."
        
        memory.add_history(session_id, "ai", initial_greeting)
        
        # Generate Audio for greeting
        audio_filename = f"{session_id}_greeting.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        
        # Use Edge TTS
        audio_generated = generate_audio_sync(initial_greeting, audio_path)
        
        return jsonify({
            "session_id": session_id,
            "message": initial_greeting,
            "audio_url": f"/audio/{audio_filename}" if audio_generated else None
        })
    except Exception as e:
        logger.error(f"Error starting interview: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/process_voice', methods=['POST'])
def process_voice():
    """Receives audio, processes it, and returns AI response."""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
            session_id = data.get('session_id')
            user_text = data.get('user_text')
            audio_file = None
        else:
            session_id = request.form.get('session_id')
            audio_file = request.files.get('audio')
            user_text = request.form.get('user_text')
        
        if not user_text:
            # If no text, try audio transcription
            if not audio_file:
                 return jsonify({"error": "No audio or text provided"}), 400
                 
            # Save user audio
            timestamp = get_timestamp()
            user_audio_filename = f"{session_id}_{timestamp}_user.wav"
            user_audio_path = os.path.join(AUDIO_FOLDER, user_audio_filename)
            audio_file.save(user_audio_path)
            
            # Transcribe
            user_text = transcribe_audio(user_audio_path)
            
        if not user_text:
            return jsonify({"error": "Could not understand audio"}), 400

            
        # Process with Interview Engine
        response_data = engine.process_answer(session_id, user_text)
        
        if "error" in response_data:
            # Fallback for API key error
            if "API Key missing" in str(response_data.get("error", "")):
                ai_text = "I cannot process your answer because the Gemini API key is missing. Please check your settings."
                response_data = {"full_text": ai_text, "difficulty": "Easy"}
            else:
                return jsonify(response_data), 500
        else:
            ai_text = response_data["full_text"]
        
        # Generate AI Audio
        # Use In-Memory TTS for speed
        import base64
        from backend.src.edge_tts_client import generate_audio_memory_sync
        
        audio_bytes = generate_audio_memory_sync(ai_text)
        
        audio_base64 = None
        if audio_bytes:
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return jsonify({
            "user_text": user_text,
            "full_text": ai_text,
            "audio_base64": audio_base64,
            "difficulty": response_data.get("difficulty", "Normal"),
            "phase": response_data.get("phase", "qa"),
            "elapsed_seconds": response_data.get("elapsed_seconds", 0),
            "interview_complete": response_data.get("interview_complete", False),
            "real_time_feedback": response_data.get("real_time_feedback", {})
        })
        
    except Exception as e:
        logger.error(f"Error processing voice: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    """Handles resume upload and parsing."""
    try:
        resume_file = request.files.get('resume')
        if not resume_file:
            return jsonify({"error": "No file uploaded"}), 400
            
        # Save file
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(filepath)
        
        # Parse
        text_content = ""
        if filename.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
        elif filename.endswith('.pdf'):
            # Use resume_analyzer to parse PDF
            text_content = resume_analyzer.parse_resume(filepath)
            
        parsed_data = parse_resume(text_content)
        parsed_data['text_content'] = text_content  # Add text content to response
        
        return jsonify(parsed_data)
        
    except Exception as e:
        logger.error(f"Error uploading profile: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/interview_results/<session_id>', methods=['GET'])
def get_interview_results(session_id):
    """Retrieves complete interview results for a session."""
    try:
        logger.info(f"Fetching results for session: {session_id}")
        session = memory.get_session(session_id)
        
        if not session:
            logger.error(f"Session not found: {session_id}")
            logger.info(f"Available sessions: {list(memory.sessions.keys())}")
            return jsonify({"error": "Session not found"}), 404
        
        logger.info(f"Session found. Keys: {session.keys()}")
        
        # Extract session data with defaults
        scores = session.get("scores", [])
        analyses = session.get("analyses", [])
        history = session.get("history", [])
        mode = session.get("mode", "HR")
        job_role = session.get("job_role", "Not specified")
        company = session.get("company", "Not specified")
        
        logger.info(f"Session data - Scores: {len(scores)}, Analyses: {len(analyses)}, History: {len(history)}")
        
        # Calculate metrics
        if scores and len(scores) > 0:
            avg_local_score = sum(s.get("local_score", 0) for s in scores) / len(scores)
            avg_ai_score = sum(s.get("ai_score", 0) for s in scores) / len(scores)
            avg_confidence = sum(s.get("confidence_score", 0) for s in scores) / len(scores)
            
            # Convert to 0-100 scale
            overall_score = int(((avg_local_score + avg_ai_score) / 20) * 100)
        else:
            # No scores yet - provide default values
            logger.warning("No scores found in session, using defaults")
            avg_local_score = 5.0
            avg_ai_score = 5.0
            avg_confidence = 50.0
            overall_score = 50
        
        # Analyze performance patterns
        total_filler_words = sum(a.get('audio', {}).get('filler_count', 0) for a in analyses)
        
        # Calculate pace statistics - handle None values
        pace_data = []
        for a in analyses:
            pace = a.get('audio', {}).get('speaking_pace', 0)
            if pace is not None and pace > 0:
                pace_data.append(pace)
        
        avg_pace = sum(pace_data) / len(pace_data) if pace_data else 0
        
        # Collect all issues and tips
        all_issues = []
        all_tips = []
        for analysis in analyses:
            audio_data = analysis.get('audio', {})
            issues = audio_data.get('issues', [])
            tips = audio_data.get('tips', [])
            if issues:
                all_issues.extend(issues)
            if tips:
                all_tips.extend(tips)
        
        # Get unique strengths and improvements
        strengths = []
        improvements = []
        
        # Add strengths based on performance - with None checks
        if avg_confidence is not None and avg_confidence >= 70:
            strengths.append("Demonstrated high confidence throughout")
        if avg_pace is not None and avg_pace >= 120 and avg_pace <= 160:
            strengths.append("Maintained optimal speaking pace")
        if total_filler_words is not None and total_filler_words < 5:
            strengths.append("Minimal use of filler words")
        if avg_ai_score is not None and avg_ai_score >= 7:
            strengths.append("Provided detailed and relevant answers")
        
        # Default strengths if none found
        if not strengths:
            strengths = [
                "Completed the interview session",
                "Engaged with the interviewer",
                "Responded to questions"
            ]
        
        # Add improvements based on performance - with None checks
        if avg_confidence is not None and avg_confidence < 60:
            improvements.append("Work on building confidence in responses")
        if avg_pace is not None and avg_pace > 0 and avg_pace < 100:
            improvements.append("Try to speak at a slightly faster pace")
        elif avg_pace is not None and avg_pace > 180:
            improvements.append("Slow down to ensure clarity")
        if total_filler_words is not None and total_filler_words >= 5:
            improvements.append("Reduce use of filler words (um, uh, like)")
        if avg_ai_score is not None and avg_ai_score < 6:
            improvements.append("Provide more specific examples and details")
        
        # Add unique tips as improvements
        unique_tips = list(set(all_tips))[:3]
        improvements.extend(unique_tips)
        
        # Default improvements if none found
        if not improvements:
            improvements = [
                "Practice more interview scenarios",
                "Work on articulating thoughts clearly",
                "Prepare specific examples from experience"
            ]
        
        # Question breakdown
        total_questions = len([h for h in history if h.get('role') == 'ai'])
        total_responses = len([h for h in history if h.get('role') == 'user'])
        
        # Calculate interview duration
        from datetime import datetime
        start_time = session.get('start_time')
        if start_time:
            duration_seconds = int((datetime.now() - start_time).total_seconds())
            duration_minutes = duration_seconds // 60
        else:
            duration_seconds = 0
            duration_minutes = 0
        
        result = {
            "session_id": session_id,
            "overall_score": overall_score,
            "mode": mode,
            "job_role": job_role,
            "company": company,
            "duration_minutes": max(1, duration_minutes),  # At least 1 minute
            "metrics": {
                "local_score": round(avg_local_score, 1),
                "ai_score": round(avg_ai_score, 1),
                "confidence": round(avg_confidence, 1),
                "speaking_pace": round(avg_pace, 1),
                "filler_words": total_filler_words,
                "total_questions": total_questions,
                "total_responses": total_responses
            },
            "strengths": strengths[:5],  # Top 5 strengths
            "improvements": improvements[:5],  # Top 5 improvements
            "score_breakdown": [
                {"category": "Content Quality", "score": round(avg_ai_score * 10, 1)},
                {"category": "Confidence", "score": round(avg_confidence, 1)},
                {"category": "Communication", "score": round(avg_local_score * 10, 1)},
                {"category": "Overall", "score": overall_score}
            ],
            "performance_trend": [s.get("ai_score", 0) * 10 for s in scores] if scores else [50]  # Scores over time
        }
        
        logger.info(f"Successfully generated results for session {session_id}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting interview results for session {session_id}: {e}", exc_info=True)
        return jsonify({"error": f"Failed to fetch results: {str(e)}"}), 500

@app.route('/final_results', methods=['POST'])
def final_results():
    """Calculates and returns final scores."""
    try:
        data = request.json
        session_id = data.get('session_id')
        session = memory.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
            
        # Calculate final scores
        scores = session.get("scores", [])
        avg_local_score = sum(s["local_score"] for s in scores) / max(1, len(scores))
        
        # Get semantic analysis of full transcript
        transcript = "\n".join([f"{h['role']}: {h['content']}" for h in session["history"]])
        semantic_data = get_semantic_score(session["mode"], str(session["resume_context"]), transcript)
        
        final_result = calculate_final_score(semantic_data, avg_local_score)
        
        # Save result to session
        memory.update_session(session_id, "final_result", final_result)
        
        return jsonify(final_result)
        
    except Exception as e:
        logger.error(f"Error getting results: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# ============================================
# HEALTH CHECK ENDPOINTS (for CI/CD)
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and CI/CD"""
    from datetime import datetime
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {}
    }
    
    # Check AI providers
    try:
        from backend.src.init_free_ai import ai_manager
        if ai_manager and ai_manager.providers:
            health_status['components']['ai_providers'] = {
                'status': 'healthy',
                'count': len(ai_manager.providers)
            }
        else:
            health_status['components']['ai_providers'] = {
                'status': 'degraded',
                'message': 'Using fallback AI'
            }
    except:
        health_status['components']['ai_providers'] = {
            'status': 'degraded',
            'message': 'Free AI not initialized'
        }
    
    # Check environment
    health_status['components']['environment'] = {
        'status': 'healthy',
        'python_version': sys.version.split()[0]
    }
    
    return jsonify(health_status), 200

@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check - is the app ready to serve traffic?"""
    return jsonify({'ready': True, 'message': 'Application is ready'}), 200

@app.route('/live', methods=['GET'])
def liveness_check():
    """Liveness check - is the app alive?"""
    from datetime import datetime
    return jsonify({'alive': True, 'timestamp': datetime.now().isoformat()}), 200


@app.route('/templates/<path:filename>')
def serve_templates(filename):
    """Serve template assets (CSS, images) from backend/templates"""
    templates_dir = os.path.join(PROJECT_ROOT, 'backend', 'templates')
    return send_from_directory(templates_dir, filename)

if __name__ == '__main__':
    # Log configuration on startup
    logger.info("="*50)
    logger.info("SAMPRO AI Interview System Starting...")
    logger.info(f"Project Root: {PROJECT_ROOT}")
    logger.info(f"Frontend Dir: {FRONTEND_DIR}")
    logger.info(f"Static Folder: {STATIC_FOLDER}")
    logger.info(f"Template Folder: {TEMPLATE_FOLDER}")
    logger.info(f"Upload Folder: {UPLOAD_FOLDER}")
    logger.info(f"Audio Folder: {AUDIO_FOLDER}")
    logger.info(f"GROQ API Key Loaded: {'Yes' if os.getenv('GROQ_API_KEY') else 'No'}")
    logger.info("="*50)
    app.run(debug=True, port=5000)
