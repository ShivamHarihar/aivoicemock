"""
Simple Test - HuggingFace Only
Tests just the HuggingFace provider to verify basic functionality
"""

import sys
import os
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.ai_provider_manager import AIProviderManager
from backend.src.response_cache import ResponseCache
from backend.src.providers.huggingface_provider import HuggingFaceProvider


async def test_huggingface():
    """Test HuggingFace provider only"""
    
    print("\n" + "="*70)
    print("TESTING HUGGINGFACE PROVIDER")
    print("="*70 + "\n")
    
    # Create AI manager
    ai_manager = AIProviderManager()
    
    # Create cache
    cache = ResponseCache(backend='memory', ttl=3600, max_size=100)
    ai_manager.set_cache(cache)
    
    # Initialize HuggingFace provider
    print("Step 1: Initializing HuggingFace provider...")
    try:
        hf_provider = HuggingFaceProvider(num_accounts=20)
        
        if not hf_provider.clients:
            print("❌ No HuggingFace API keys found!")
            print("\nPlease add to your .env file:")
            print("  HF_API_KEY_1=hf_your_key_here")
            print("  HF_API_KEY_2=hf_your_key_here")
            return False
        
        ai_manager.register_provider('huggingface', hf_provider)
        print(f"✓ HuggingFace initialized with {len(hf_provider.clients)} accounts")
        print(f"  Model: {hf_provider.current_model}")
        print()
        
    except Exception as e:
        print(f"❌ HuggingFace initialization failed: {e}")
        return False
    
    # Test simple request
    print("Step 2: Testing AI response...")
    
    test_prompt = "Say 'Hello, I am working!' in a friendly way."
    
    try:
        response = await ai_manager.get_response(
            prompt=test_prompt,
            context="You are a helpful AI assistant."
        )
        
        print(f"✓ Response received:")
        print(f"  {response[:200]}...")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Show stats
    print("="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\n✅ HuggingFace provider is working!")
    print(f"   Accounts: {len(hf_provider.clients)}")
    print(f"   Daily capacity: ~{len(hf_provider.clients) * 20000:,} requests/day")
    print(f"   Can handle: ~{len(hf_provider.clients) * 20000 // 17:,} interviews/day")
    print()
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_huggingface())
        
        if result:
            print("🎉 HuggingFace is ready!")
            print("\nNext: Add Groq keys to increase capacity")
            sys.exit(0)
        else:
            print("\n⚠️  Please configure HuggingFace API keys")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
