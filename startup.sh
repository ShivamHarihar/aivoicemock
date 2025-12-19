#!/bin/bash

# Azure App Service Startup Script
# This script runs when the container starts

echo "Starting Sampro Interview System..."

# Navigate to app directory
cd /home/site/wwwroot

# Set Python path
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH

# Install dependencies if needed
if [ -f "backend/requirements.txt" ]; then
    echo "Installing backend dependencies..."
    pip install --no-cache-dir -r backend/requirements.txt
fi

if [ -f "backend/requirements_free_ai.txt" ]; then
    echo "Installing free AI dependencies..."
    pip install --no-cache-dir -r backend/requirements_free_ai.txt
fi

# Initialize free AI system
echo "Initializing Free AI System..."
python -c "from backend.src.init_free_ai import initialize_free_ai_system; initialize_free_ai_system()" || echo "Free AI initialization skipped"

# Start Gunicorn
echo "Starting Gunicorn server..."
cd backend/app

# Use environment variable for workers, default to 4
WORKERS=${GUNICORN_WORKERS:-4}

exec gunicorn \
    --config ../../gunicorn_config.py \
    --workers $WORKERS \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
