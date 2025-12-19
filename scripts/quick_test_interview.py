"""
Quick Test Script for Sampro AI Interview Platform
Tests the 4-minute interview (2 min Q&A + 2 min summary)
"""

import requests
import time
import json

# Configuration
BASE_URL = "http://localhost:5000"
TEST_MODE = "Technical"
TEST_JOB_ROLE = "Software Engineer"
TEST_COMPANY = "Google"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_interview_timing():
    """Test the interview with timing verification"""
    
    print_section("QUICK INTERVIEW TEST - 4 MINUTES TOTAL")
    print("Configuration:")
    print(f"  - Q&A Phase: 2 minutes")
    print(f"  - Summary Phase: 2 minutes")
    print(f"  - Total Duration: 4 minutes")
    print(f"  - Mode: {TEST_MODE}")
    print(f"  - Role: {TEST_JOB_ROLE}")
    print(f"  - Company: {TEST_COMPANY}")
    
    # Step 1: Start Interview
    print_section("Step 1: Starting Interview")
    try:
        response = requests.post(
            f"{BASE_URL}/start_call_interview",
            json={
                "mode": TEST_MODE,
                "job_role": TEST_JOB_ROLE,
                "company": TEST_COMPANY
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to start interview: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        data = response.json()
        session_id = data.get("session_id")
        greeting = data.get("message")
        
        print(f"✅ Interview started successfully!")
        print(f"Session ID: {session_id}")
        print(f"AI Greeting: {greeting[:100]}...")
        
    except Exception as e:
        print(f"❌ Error starting interview: {e}")
        return
    
    # Step 2: Simulate Q&A Phase (2 minutes)
    print_section("Step 2: Q&A Phase (2 minutes)")
    print("Sending test answers every 30 seconds...")
    
    test_answers = [
        "I am a software engineer with 5 years of experience in Python and JavaScript.",
        "I have worked on several web applications using React and Django frameworks.",
        "My biggest achievement was building a scalable microservices architecture.",
        "I enjoy solving complex problems and learning new technologies."
    ]
    
    start_time = time.time()
    qa_duration = 120  # 2 minutes in seconds
    
    for i, answer in enumerate(test_answers):
        elapsed = time.time() - start_time
        
        # Check if we've exceeded Q&A phase
        if elapsed >= qa_duration:
            print(f"\n⏰ Q&A phase should end at {qa_duration}s, elapsed: {elapsed:.1f}s")
            break
        
        print(f"\n[{elapsed:.1f}s] Sending answer #{i+1}: {answer[:50]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/process_voice",
                json={
                    "session_id": session_id,
                    "user_text": answer
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                phase = data.get("phase", "qa")
                elapsed_seconds = data.get("elapsed_seconds", 0)
                ai_response = data.get("full_text", "")
                
                print(f"✅ Response received")
                print(f"   Phase: {phase}")
                print(f"   Elapsed: {elapsed_seconds}s")
                print(f"   AI: {ai_response[:80]}...")
                
                # Check if we've transitioned to summary
                if phase == "summary":
                    print(f"\n🎉 Summary phase triggered at {elapsed_seconds}s!")
                    print(f"   Expected: ~{qa_duration}s")
                    print(f"   Difference: {abs(elapsed_seconds - qa_duration)}s")
                    break
            else:
                print(f"❌ Error: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Error processing answer: {e}")
        
        # Wait before next answer (simulate thinking time)
        if i < len(test_answers) - 1:
            wait_time = 30
            print(f"   Waiting {wait_time}s before next answer...")
            time.sleep(wait_time)
    
    # Step 3: Trigger Summary Phase
    print_section("Step 3: Summary Phase (should trigger at ~2 minutes)")
    
    # Wait until we're past the Q&A phase
    elapsed = time.time() - start_time
    if elapsed < qa_duration:
        wait_time = qa_duration - elapsed + 5  # Wait until past Q&A phase
        print(f"Waiting {wait_time:.1f}s to reach summary phase...")
        time.sleep(wait_time)
    
    # Send one more answer to trigger summary
    print("\nSending final answer to trigger summary...")
    try:
        response = requests.post(
            f"{BASE_URL}/process_voice",
            json={
                "session_id": session_id,
                "user_text": "I am very excited about this opportunity and look forward to contributing to the team."
            },
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            phase = data.get("phase", "qa")
            elapsed_seconds = data.get("elapsed_seconds", 0)
            interview_complete = data.get("interview_complete", False)
            summary = data.get("full_text", "")
            
            print(f"✅ Summary phase response received")
            print(f"   Phase: {phase}")
            print(f"   Elapsed: {elapsed_seconds}s")
            print(f"   Interview Complete: {interview_complete}")
            print(f"\n📊 Performance Summary:")
            print(f"   {summary[:200]}...")
            
            if phase == "summary" and interview_complete:
                print(f"\n🎉 SUCCESS! Interview completed in {elapsed_seconds}s")
                print(f"   Expected: ~{qa_duration + 120}s (4 minutes)")
            else:
                print(f"\n⚠️  Phase is '{phase}', expected 'summary'")
        else:
            print(f"❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error triggering summary: {e}")
    
    # Step 4: Get Final Results
    print_section("Step 4: Getting Final Results")
    try:
        response = requests.post(
            f"{BASE_URL}/final_results",
            json={"session_id": session_id},
            timeout=15
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Final results retrieved")
            print(f"\n📈 Scores:")
            print(f"   Final Score: {results.get('final_score', 'N/A')}/10")
            print(f"   Local Score: {results.get('local_score', 'N/A')}/10")
            print(f"   Gemini Score: {results.get('gemini_score', 'N/A')}/10")
            
            strengths = results.get('strengths', [])
            if strengths:
                print(f"\n💪 Strengths:")
                for s in strengths[:3]:
                    print(f"   - {s}")
            
            weaknesses = results.get('weaknesses', [])
            if weaknesses:
                print(f"\n📝 Areas for Improvement:")
                for w in weaknesses[:3]:
                    print(f"   - {w}")
        else:
            print(f"❌ Error getting results: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error getting final results: {e}")
    
    # Summary
    total_time = time.time() - start_time
    print_section("TEST SUMMARY")
    print(f"✅ Test completed in {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print(f"   Expected: ~4 minutes (240 seconds)")
    print(f"   Session ID: {session_id}")
    print(f"\n✨ Interview timing is configured for quick testing!")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          SAMPRO AI INTERVIEW - QUICK TEST SCRIPT                    ║
║                                                                      ║
║  This script tests the 4-minute interview configuration:            ║
║  - 2 minutes Q&A phase                                              ║
║  - 2 minutes summary phase                                          ║
║                                                                      ║
║  Make sure the Flask server is running on http://localhost:5000     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!\n")
            test_interview_timing()
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server!")
        print(f"   Please make sure Flask is running on {BASE_URL}")
        print("   Run: cd backend/app && python app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")
