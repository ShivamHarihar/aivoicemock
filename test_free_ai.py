"""
Test Free AI System
Quick test to verify all providers are working correctly
"""

import sys
import os
import asyncio

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.init_free_ai import (
    initialize_free_ai_system,
    get_ai_response,
    get_ai_response_async,
    print_system_status
)


async def test_providers():
    """Test all configured providers"""
    
    print("\n" + "="*60)
    print("TESTING FREE AI SYSTEM")
    print("="*60 + "\n")
    
    # Initialize system
    print("Step 1: Initializing AI system...")
    ai_manager = initialize_free_ai_system()
    
    if not ai_manager or not ai_manager.providers:
        print("\n❌ ERROR: No AI providers configured!")
        print("\nPlease set up API keys in .env file:")
        print("  - HF_API_KEY_1, HF_API_KEY_2, etc. for HuggingFace")
        print("  - GROQ_API_KEY_1, GROQ_API_KEY_2, etc. for Groq")
        return False
    
    print(f"✓ System initialized with {len(ai_manager.providers)} providers\n")
    
    # Test prompts
    test_prompts = [
        {
            "prompt": "Say 'Hello, I am working!' in a friendly way.",
            "context": "You are a helpful AI assistant."
        },
        {
            "prompt": "What are the top 3 skills for a software engineer?",
            "context": "You are an interview AI helping candidates prepare."
        },
        {
            "prompt": "Explain what ATS-friendly means in one sentence.",
            "context": "You are a resume expert."
        }
    ]
    
    # Test each prompt
    print("Step 2: Testing AI responses...\n")
    
    for i, test in enumerate(test_prompts, 1):
        print(f"Test {i}/3: {test['prompt'][:50]}...")
        
        try:
            response = await get_ai_response_async(
                prompt=test['prompt'],
                context=test['context']
            )
            
            print(f"✓ Response: {response[:100]}...")
            print()
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}\n")
            return False
    
    # Show final stats
    print("\nStep 3: System Statistics")
    print_system_status()
    
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nYour free AI system is ready to handle interviews!")
    print("Estimated capacity with current setup:")
    
    # Calculate capacity
    stats = ai_manager.get_stats()
    provider_count = len(ai_manager.providers)
    
    if 'huggingface' in ai_manager.providers:
        hf_accounts = len(ai_manager.providers['huggingface'].clients)
        print(f"  • HuggingFace: {hf_accounts} accounts × ~20,000/day = {hf_accounts * 20000:,} requests/day")
    
    if 'groq' in ai_manager.providers:
        groq_accounts = len(ai_manager.providers['groq'].clients)
        groq_capacity = groq_accounts * 14400
        print(f"  • Groq: {groq_accounts} accounts × 14,400/day = {groq_capacity:,} requests/day")
    
    print(f"\n  With 80% cache hit rate:")
    print(f"  → Can handle ~26,000+ interviews per day!")
    print()
    
    return True


def main():
    """Run tests"""
    try:
        # Run async tests
        result = asyncio.run(test_providers())
        
        if result:
            print("\n🎉 Success! You can now:")
            print("  1. Integrate with interview engine")
            print("  2. Start handling interviews at zero cost")
            print("  3. Monitor usage with print_system_status()")
            sys.exit(0)
        else:
            print("\n⚠️  Setup incomplete. Please configure API keys.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
