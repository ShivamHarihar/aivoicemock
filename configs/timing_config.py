"""
Interview Timing Configuration Guide
=====================================

This file explains how to configure interview timing for different scenarios.
"""

# ============================================================================
# TIMING CONFIGURATIONS
# ============================================================================

# QUICK TEST MODE (Current Setting)
# ----------------------------------
# Total Duration: 4 minutes
# Q&A Phase: 2 minutes
# Summary Phase: 2 minutes
# 
# Use for: Quick testing, development, debugging
# 
# To enable: In backend/src/interview_engine.py, set:
#   INTERVIEW_DURATION_MINUTES = 4
#   QA_PHASE_MINUTES = 2

QUICK_TEST = {
    "INTERVIEW_DURATION_MINUTES": 4,
    "QA_PHASE_MINUTES": 2,
    "description": "Quick testing mode - 2 min Q&A + 2 min summary",
    "expected_questions": "2-3 questions",
    "use_case": "Development and quick testing"
}

# STANDARD TEST MODE
# ------------------
# Total Duration: 10 minutes
# Q&A Phase: 7 minutes
# Summary Phase: 3 minutes
# 
# Use for: Moderate testing, demo purposes
# 
# To enable: In backend/src/interview_engine.py, set:
#   INTERVIEW_DURATION_MINUTES = 10
#   QA_PHASE_MINUTES = 7

STANDARD_TEST = {
    "INTERVIEW_DURATION_MINUTES": 10,
    "QA_PHASE_MINUTES": 7,
    "description": "Standard testing mode - 7 min Q&A + 3 min summary",
    "expected_questions": "5-7 questions",
    "use_case": "Demo and moderate testing"
}

# PRODUCTION MODE (Full Interview)
# ---------------------------------
# Total Duration: 20 minutes
# Q&A Phase: 15 minutes
# Summary Phase: 5 minutes
# 
# Use for: Real interview practice, production deployment
# 
# To enable: In backend/src/interview_engine.py, set:
#   INTERVIEW_DURATION_MINUTES = 20
#   QA_PHASE_MINUTES = 15

PRODUCTION = {
    "INTERVIEW_DURATION_MINUTES": 20,
    "QA_PHASE_MINUTES": 15,
    "description": "Production mode - 15 min Q&A + 5 min summary",
    "expected_questions": "8-12 questions",
    "use_case": "Real interview practice"
}

# EXTENDED MODE (Comprehensive Interview)
# ----------------------------------------
# Total Duration: 30 minutes
# Q&A Phase: 25 minutes
# Summary Phase: 5 minutes
# 
# Use for: In-depth practice, multiple rounds
# 
# To enable: In backend/src/interview_engine.py, set:
#   INTERVIEW_DURATION_MINUTES = 30
#   QA_PHASE_MINUTES = 25

EXTENDED = {
    "INTERVIEW_DURATION_MINUTES": 30,
    "QA_PHASE_MINUTES": 25,
    "description": "Extended mode - 25 min Q&A + 5 min summary",
    "expected_questions": "12-15 questions",
    "use_case": "In-depth interview practice"
}

# ============================================================================
# HOW TO CHANGE TIMING
# ============================================================================

"""
Step 1: Open the file
---------------------
File: backend/src/interview_engine.py

Step 2: Find the timing constants (around line 10-13)
------------------------------------------------------
Look for:
    # Interview timing constants (configurable for testing)
    INTERVIEW_DURATION_MINUTES = 4  # Total interview time
    QA_PHASE_MINUTES = 2  # Q&A phase duration

Step 3: Update the values
--------------------------
Change to your desired configuration:

For Quick Test (4 min):
    INTERVIEW_DURATION_MINUTES = 4
    QA_PHASE_MINUTES = 2

For Standard Test (10 min):
    INTERVIEW_DURATION_MINUTES = 10
    QA_PHASE_MINUTES = 7

For Production (20 min):
    INTERVIEW_DURATION_MINUTES = 20
    QA_PHASE_MINUTES = 15

For Extended (30 min):
    INTERVIEW_DURATION_MINUTES = 30
    QA_PHASE_MINUTES = 25

Step 4: Restart the server
---------------------------
Stop the Flask server (Ctrl+C) and restart:
    cd backend/app
    python app.py

Step 5: Test the new timing
----------------------------
Run the quick test script:
    python scripts/quick_test_interview.py

Or start a new interview through the web interface.
"""

# ============================================================================
# TIMING CALCULATION
# ============================================================================

"""
How timing works:
-----------------

1. Interview starts when user clicks "Start Interview"
2. Timer starts counting from 0
3. Q&A Phase runs from 0 to QA_PHASE_MINUTES
4. Summary Phase triggers at QA_PHASE_MINUTES
5. Interview completes at INTERVIEW_DURATION_MINUTES

Example with QUICK_TEST (4 min):
---------------------------------
0:00 - Interview starts
0:00 - 2:00 - Q&A Phase (AI asks questions)
2:00 - 4:00 - Summary Phase (AI gives feedback)
4:00 - Interview complete

Example with PRODUCTION (20 min):
----------------------------------
0:00 - Interview starts
0:00 - 15:00 - Q&A Phase (AI asks questions)
15:00 - 20:00 - Summary Phase (AI gives feedback)
20:00 - Interview complete
"""

# ============================================================================
# TESTING RECOMMENDATIONS
# ============================================================================

"""
For Development:
----------------
Use QUICK_TEST (4 min)
- Fast iteration
- Quick bug testing
- Feature development

For Demo/Presentation:
----------------------
Use STANDARD_TEST (10 min)
- Shows full flow
- Not too long for audience
- Demonstrates all features

For User Testing:
-----------------
Use PRODUCTION (20 min)
- Realistic experience
- Proper evaluation
- Complete feedback

For Stress Testing:
-------------------
Use EXTENDED (30 min)
- Test system stability
- Long session handling
- Memory management
"""

# ============================================================================
# CURRENT CONFIGURATION
# ============================================================================

CURRENT_CONFIG = QUICK_TEST

print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          CURRENT INTERVIEW TIMING CONFIGURATION                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Mode: {CURRENT_CONFIG['description']}
Total Duration: {CURRENT_CONFIG['INTERVIEW_DURATION_MINUTES']} minutes
Q&A Phase: {CURRENT_CONFIG['QA_PHASE_MINUTES']} minutes
Summary Phase: {CURRENT_CONFIG['INTERVIEW_DURATION_MINUTES'] - CURRENT_CONFIG['QA_PHASE_MINUTES']} minutes
Expected Questions: {CURRENT_CONFIG['expected_questions']}
Use Case: {CURRENT_CONFIG['use_case']}

To change configuration:
1. Edit: backend/src/interview_engine.py
2. Update: INTERVIEW_DURATION_MINUTES and QA_PHASE_MINUTES
3. Restart: Flask server
4. Test: Run scripts/quick_test_interview.py

Available Modes:
- QUICK_TEST: 4 min (2 min Q&A + 2 min summary)
- STANDARD_TEST: 10 min (7 min Q&A + 3 min summary)
- PRODUCTION: 20 min (15 min Q&A + 5 min summary)
- EXTENDED: 30 min (25 min Q&A + 5 min summary)

╚══════════════════════════════════════════════════════════════════════╝
""")
