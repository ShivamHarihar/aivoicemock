import logging
import os

logger = logging.getLogger(__name__)

try:
    import torch
except ImportError:
    torch = None
    logger.warning("Torch not installed. TTS will be disabled.")

try:
    from TTS.api import TTS
except ImportError:
    TTS = None
    logger.warning("Coqui TTS not installed. Audio generation will be disabled.")

# Initialize TTS
# Using a fast and good quality model. 'tts_models/en/ljspeech/glow-tts' is a common choice, 
# but 'tts_models/multilingual/multi-dataset/xtts_v2' is state of the art for expressiveness if available and hardware allows.
# For standard CPU/lightweight, we might use a simpler one.
# Let's use a standard reliable one for now to ensure it runs.
MODEL_NAME = "tts_models/en/ljspeech/vits" 

tts = None
if TTS:
    try:
        # gpu=False for compatibility, can be True if CUDA available
        tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)
        logger.info(f"Coqui TTS model {MODEL_NAME} loaded.")
    except Exception as e:
        logger.error(f"Failed to load Coqui TTS model: {e}")
        tts = None
else:
    logger.warning("TTS module not available, model loading skipped.")

def generate_audio(text, output_path):
    """Generates audio from text and saves to output_path."""
    if not tts:
        logger.error("TTS model is not loaded.")
        return False

    try:
        # Generate audio
        tts.tts_to_file(text=text, file_path=output_path)
        logger.info(f"Audio generated at {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return False
