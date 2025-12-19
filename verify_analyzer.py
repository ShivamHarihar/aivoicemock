import sys
import os
import logging
from unittest.mock import patch, MagicMock

# Setup paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)

# Mock logger
logging.basicConfig(level=logging.INFO)

from backend.src.resume_analyzer import analyze_resume_content

def test_analyzer_logic():
    print("Testing analyze_resume_content with mocked LLM response...")
    
    # Mock data that simulates the new prompt output
    mock_llm_response = {
        "overall_score": 85,
        "summary": "Great candidate.",
        "structured_data": {
            "personal_info": {
                "name": "AI Generated Name",
                "email": "ai.generated@test.com",
                "phone": "999-999-9999",
                "location": "Metaverse"
            },
            "experience": [
                {"title": "AI Engineer", "company": "Future Corp", "description": "Built AGI"}
            ],
            "skills": {
                "languages": ["Python", "Rust"],
                "frameworks": ["PyTorch"]
            }
        }
    }
    
    # Patch the generate_resume_analysis function
    with patch('backend.src.resume_analyzer.generate_resume_analysis') as mock_generate:
        mock_generate.return_value = mock_llm_response
        
        # Test input (must be > 50 chars)
        sample_text = "Original Name\noriginal@test.com\n" + "x" * 50
        
        # Call the function
        result = analyze_resume_content(sample_text)
        
        print("\n=== DEBUG: Full Analyzer Result ===")
        import pprint
        pprint.pprint(result)
        print("===================================")
        
        print("\nAnalyzer Result Keys:", result.keys())
        
        # Verify priority (AI data should overwrite regex data from sample_text)
        print(f"Candidate Name: {result.get('candidate_name')}")
        assert result.get('candidate_name') == "AI Generated Name", f"Expected 'AI Generated Name', got '{result.get('candidate_name')}'"
        
        print(f"Email: {result.get('email')}")
        assert result.get('email') == "ai.generated@test.com", f"Expected 'ai.generated@test.com', got '{result.get('email')}'"
        
        print(f"Extracted Skills: {result.get('extracted_skills')}")
        assert "languages" in result.get('extracted_skills')
        
        print(f"Structured Resume Present: {'structured_resume' in result}")
        assert 'structured_resume' in result
        
        print("\n✅ Verification Successful! Logic correctly prioritizes LLM data.")

if __name__ == "__main__":
    test_analyzer_logic()
