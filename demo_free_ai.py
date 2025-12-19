"""
Free AI System Demo
Demonstrates the system working with mock providers (no API keys needed for demo)
"""

import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.ai_provider_manager import AIProviderManager, BaseAIProvider, UsageTracker
from backend.src.response_cache import ResponseCache


class MockProvider(BaseAIProvider):
    """Mock AI provider for demonstration"""
    
    def __init__(self, name, responses_per_day=1000):
        super().__init__(name)
        self.daily_limit = responses_per_day
        self.mock_responses = [
            "That's a great question! Let me think about that...",
            "Based on your experience, I'd say you have strong potential in this area.",
            "Can you tell me more about your approach to problem-solving?",
            "Your background in technology is impressive. How do you stay current with new developments?",
            "I appreciate your detailed response. Let's explore this further."
        ]
        self.response_index = 0
    
    async def generate(self, prompt, context=None, max_tokens=500, temperature=0.7):
        """Generate mock response"""
        await asyncio.sleep(0.1)  # Simulate API delay
        
        response = self.mock_responses[self.response_index % len(self.mock_responses)]
        self.response_index += 1
        self.request_count += 1
        
        return f"{response} (from {self.name})"


async def demo():
    """Run demonstration"""
    
    print("\n" + "="*70)
    print("FREE AI INTERVIEW SYSTEM - DEMO")
    print("="*70)
    print("\n📝 This demo shows how the system works WITHOUT real API keys")
    print("   Using mock providers to demonstrate functionality\n")
    
    # Create AI manager
    ai_manager = AIProviderManager()
    
    # Create cache
    cache = ResponseCache(backend='memory', ttl=3600, max_size=100)
    ai_manager.set_cache(cache)
    
    # Register mock providers
    print("Step 1: Registering AI Providers...")
    providers = [
        MockProvider("HuggingFace-1", 20000),
        MockProvider("HuggingFace-2", 20000),
        MockProvider("Groq-1", 14400),
        MockProvider("Groq-2", 14400),
    ]
    
    for provider in providers:
        ai_manager.register_provider(provider.name.lower().replace('-', '_'), provider)
        print(f"  ✓ {provider.name}: {provider.daily_limit:,} requests/day")
    
    total_capacity = sum(p.daily_limit for p in providers)
    print(f"\n  Total Daily Capacity: {total_capacity:,} requests")
    print(f"  With 80% cache: {int(total_capacity / 0.2):,} effective requests/day")
    print(f"  Can handle: ~{int(total_capacity / 0.2 / 17):,} interviews/day\n")
    
    # Simulate interview questions
    print("Step 2: Simulating Interview Questions...\n")
    
    interview_prompts = [
        ("Tell me about yourself", "You are an AI interviewer"),
        ("What are your strengths?", "You are an AI interviewer"),
        ("Describe a challenging project", "You are an AI interviewer"),
        ("Tell me about yourself", "You are an AI interviewer"),  # Duplicate - should hit cache
        ("What are your career goals?", "You are an AI interviewer"),
    ]
    
    for i, (prompt, context) in enumerate(interview_prompts, 1):
        print(f"Question {i}: {prompt}")
        
        try:
            response = await ai_manager.get_response(prompt, context)
            print(f"Response: {response}")
            print()
            
        except Exception as e:
            print(f"Error: {e}\n")
    
    # Show statistics
    print("="*70)
    print("SYSTEM STATISTICS")
    print("="*70 + "\n")
    
    stats = ai_manager.get_stats()
    cache_stats = cache.get_stats()
    
    print(f"📊 Overall Performance:")
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Cache Hit Rate: {stats.get('cache_hit_rate', 0):.1f}%")
    print(f"  Cache Hits: {stats['cache_hits']}")
    print(f"  Cache Misses: {stats['cache_misses']}")
    
    print(f"\n🤖 Provider Usage:")
    for provider_name, count in stats['provider_requests'].items():
        print(f"  {provider_name}: {count} requests")
    
    print(f"\n💡 Cost Savings:")
    print(f"  If using paid API (e.g., GPT-4 at $0.03/request):")
    print(f"  Cost with paid API: ${stats['total_requests'] * 0.03:.2f}")
    print(f"  Cost with free system: $0.00")
    print(f"  Savings: ${stats['total_requests'] * 0.03:.2f}")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\n📌 Next Steps:")
    print("  1. Get free API keys from HuggingFace and Groq")
    print("  2. Add keys to .env file")
    print("  3. Run: python test_free_ai.py")
    print("  4. Start handling real interviews at ZERO cost!")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
