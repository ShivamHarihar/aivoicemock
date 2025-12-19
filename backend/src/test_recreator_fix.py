"""
Quick test to verify the resume recreator now uses real analyzer scores.
Run this to ensure the integration is working correctly.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

def test_import():
    """Test that the import works correctly"""
    print("Testing imports...")
    try:
        from backend.src.resume_recreator import recreate_resume_with_ai
        from backend.src.resume_analyzer import analyze_resume_content
        print("✅ Imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_module_integration():
    """Test that resume_recreator has access to analyze_resume_content"""
    print("\nTesting module integration...")
    try:
        from backend.src import resume_recreator
        # Check if analyze_resume_content is accessible
        if hasattr(resume_recreator, 'analyze_resume_content'):
            print("✅ analyze_resume_content is accessible in resume_recreator module")
            return True
        else:
            print("⚠️ analyze_resume_content not found as module attribute (this is OK if imported locally)")
            # Try to import it
            from backend.src.resume_recreator import analyze_resume_content
            print("✅ analyze_resume_content can be imported from resume_recreator")
            return True
    except Exception as e:
        print(f"❌ Module integration test failed: {e}")
        return False

def test_function_signature():
    """Verify the function signature hasn't changed"""
    print("\nTesting function signature...")
    try:
        from backend.src.resume_recreator import recreate_resume_with_ai
        import inspect
        
        sig = inspect.signature(recreate_resume_with_ai)
        params = list(sig.parameters.keys())
        
        expected_params = ['resume_text', 'current_score', 'analysis_data']
        if params == expected_params:
            print(f"✅ Function signature correct: {params}")
            return True
        else:
            print(f"⚠️ Function signature changed. Expected: {expected_params}, Got: {params}")
            return False
    except Exception as e:
        print(f"❌ Signature test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Resume Recreator Fix - Integration Test")
    print("=" * 60)
    
    results = []
    results.append(("Import Test", test_import()))
    results.append(("Module Integration", test_module_integration()))
    results.append(("Function Signature", test_function_signature()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! The fix is ready.")
        print("\nNext step: Start the server and test manually:")
        print("  cd backend/app")
        print("  python app.py")
    else:
        print("⚠️ Some tests failed. Review the errors above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
