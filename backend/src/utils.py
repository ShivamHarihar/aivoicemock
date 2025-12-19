import os
import uuid
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_session_id():
    """Generates a unique session ID."""
    return str(uuid.uuid4())

def save_json(data, filepath):
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved JSON to {filepath}")
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")

def load_json(filepath):
    """Loads data from a JSON file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        logger.error(f"Error loading JSON from {filepath}: {e}")
        return None

def ensure_directory(path):
    """Ensures a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")

def get_timestamp():
    """Returns current timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
