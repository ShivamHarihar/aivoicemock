#!/usr/bin/env python
"""
Comprehensive System Test
Tests all major functionality of the SAMPRO AI Interview System
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

print("="*60)
print("SAMPRO AI Interview System - Comprehensive Test")
print("="*60)

# Test 1: Environment Variables
print("\n[TEST 1] Environment Variables")
print("-" * 40)
groq_key = os.getenv('GROQ_API_KEY')
if groq_key:
    print(f"✅ GROQ_API_KEY loaded (length: {len(groq_key)})")
else:
    print("❌ GROQ_API_KEY not found!")

# Test 2: Module Imports
print("\n[TEST 2] Module Imports")
print("-" * 40)
try:
    from backend.src.grok_client import generate_response, generate_resume_analysis
    print("✅ grok_client imported successfully")
except Exception as e:
    print(f"❌ grok_client import failed: {e}")

try:
    from backend.src.prompts import SYSTEM_INSTRUCTION, DETAILED_RESUME_ANALYSIS_PROMPT
    print("✅ prompts imported successfully")
except Exception as e:
    print(f"❌ prompts import failed: {e}")

try:
    from backend.src.resume_analyzer import parse_resume, analyze_resume_content
    print("✅ resume_analyzer imported successfully")
except Exception as e:
    print(f"❌ resume_analyzer import failed: {e}")

try:
    from backend.src.resume_recreator import recreate_resume_with_ai
    print("✅ resume_recreator imported successfully")
except Exception as e:
    print(f"❌ resume_recreator import failed: {e}")

try:
    from backend.src.interview_engine import engine
    print("✅ interview_engine imported successfully")
except Exception as e:
    print(f"❌ interview_engine import failed: {e}")

# Test 3: File Paths
print("\n[TEST 3] File Paths")
print("-" * 40)
frontend_dir = os.path.join(PROJECT_ROOT, 'frontend')
static_dir = os.path.join(frontend_dir, 'public')
template_dir = os.path.join(frontend_dir, 'src')

print(f"Frontend Dir: {frontend_dir}")
print(f"  Exists: {'✅' if os.path.exists(frontend_dir) else '❌'}")

print(f"Static Dir: {static_dir}")
print(f"  Exists: {'✅' if os.path.exists(static_dir) else '❌'}")

print(f"Template Dir: {template_dir}")
print(f"  Exists: {'✅' if os.path.exists(template_dir) else '❌'}")

# Test 4: API Connection (if key exists)
if groq_key:
    print("\n[TEST 4] API Connection Test")
    print("-" * 40)
    try:
        from backend.src.grok_client import generate_text_response
        test_prompt = "Say 'Hello' in one word."
        print("Testing Groq API connection...")
        response = generate_text_response(test_prompt)
        if response and "API Key missing" not in response:
            print(f"✅ API Response: {response[:50]}...")
        else:
            print(f"❌ API Error: {response}")
    except Exception as e:
        print(f"❌ API Test failed: {e}")
else:
    print("\n[TEST 4] API Connection Test")
    print("-" * 40)
    print("⏭️  Skipped (no API key)")

# Test 5: Resume Analysis (sample)
print("\n[TEST 5] Resume Analysis Test")
print("-" * 40)
sample_resume = """
John Doe
Software Engineer
Email: john@example.com

EXPERIENCE:
Software Engineer at Tech Corp (2020-2023)
- Developed web applications using Python and React
- Led team of 3 developers
- Improved system performance by 40%

SKILLS:
Python, JavaScript, React, Node.js, SQL

EDUCATION:
BS Computer Science, University of Tech, 2020
"""

try:
    from backend.src.resume_analyzer import analyze_resume_content
    print("Analyzing sample resume...")
    # Note: This will fail without API key, but tests the function
    result = analyze_resume_content(sample_resume)
    if "error" not in result or "API Key" not in str(result.get("error", "")):
        print(f"✅ Analysis completed: Score = {result.get('overall_score', 'N/A')}")
    else:
        print(f"⚠️  Analysis requires API key: {result.get('error', '')}")
except Exception as e:
    print(f"❌ Analysis test failed: {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("\n✅ = Pass | ❌ = Fail | ⚠️  = Warning | ⏭️  = Skipped\n")
print("Next Steps:")
print("1. Ensure GROQ_API_KEY is set in .env file")
print("2. Run: python backend/app/app.py")
print("3. Open: http://localhost:5000")
print("4. Test resume analysis and interview features")
print("\n" + "="*60)
