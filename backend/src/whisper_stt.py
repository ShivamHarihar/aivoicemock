import logging
import os

logger = logging.getLogger(__name__)

try:
    import whisper
except ImportError:
    whisper = None
    logger.info("Whisper not installed. Using browser's built-in speech recognition (works great!).")

# Load model globally to avoid reloading per request
# Using 'base' model for balance of speed and accuracy. Can be 'tiny', 'small', 'medium', 'large'.
model = None
if whisper:
    try:
        model = whisper.load_model("base")
        logger.info("Whisper model loaded successfully - advanced audio transcription available.")
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        model = None
else:
    logger.info("Using browser-based speech recognition (primary method).")

def transcribe_audio(file_path):
    """Transcribes audio file to text using Whisper."""
    if not model:
        logger.error("Whisper model is not loaded.")
        return None

    try:
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return None

        # Whisper handles noise reduction and normalization internally to some extent
        result = model.transcribe(file_path, fp16=False) # fp16=False for CPU compatibility if needed
        text = result.get("text", "").strip()
        logger.info(f"Transcription successful: {text[:50]}...")
        return text
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        return None
