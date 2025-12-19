"""
Initialize Free AI System
Sets up all AI providers and integrates with the interview system
"""

import logging
from backend.src.ai_provider_manager import ai_manager
from backend.src.response_cache import response_cache
from backend.src.providers.huggingface_provider import HuggingFaceProvider
from backend.src.providers.groq_provider import GroqProvider

logger = logging.getLogger(__name__)


def initialize_free_ai_system():
    """
    Initialize the free AI system with all providers
    
    This function:
    1. Sets up response caching
    2. Initializes all AI providers
    3. Registers providers with the AI manager
    4. Returns the configured AI manager
    """
    
    logger.info("=" * 60)
    logger.info("Initializing Free AI Interview System")
    logger.info("=" * 60)
    
    # Step 1: Setup caching
    logger.info("Setting up response cache...")
    ai_manager.set_cache(response_cache)
    logger.info(f"✓ Cache configured: {response_cache.backend} backend")
    
    # Step 2: Initialize HuggingFace provider
    logger.info("Initializing HuggingFace provider...")
    try:
        hf_provider = HuggingFaceProvider(num_accounts=20)
        if hf_provider.clients:
            ai_manager.register_provider('huggingface', hf_provider)
            logger.info(f"✓ HuggingFace: {len(hf_provider.clients)} accounts ready")
        else:
            logger.warning("✗ HuggingFace: No API keys found")
    except Exception as e:
        logger.error(f"✗ HuggingFace initialization failed: {e}")
    
    # Step 3: Initialize Groq provider
    logger.info("Initializing Groq provider...")
    try:
        groq_provider = GroqProvider(num_accounts=10)
        if groq_provider.clients:
            ai_manager.register_provider('groq', groq_provider)
            logger.info(f"✓ Groq: {len(groq_provider.clients)} accounts ready")
            logger.info(f"  Daily capacity: {groq_provider.daily_limit:,} requests")
        else:
            logger.warning("✗ Groq: No API keys found")
    except Exception as e:
        logger.error(f"✗ Groq initialization failed: {e}")
    
    # Step 4: Check if we have at least one provider
    if not ai_manager.providers:
        logger.error("!" * 60)
        logger.error("NO AI PROVIDERS AVAILABLE!")
        logger.error("Please set up at least one provider:")
        logger.error("  - HuggingFace: Set HF_API_KEY_1, HF_API_KEY_2, etc.")
        logger.error("  - Groq: Set GROQ_API_KEY_1, GROQ_API_KEY_2, etc.")
        logger.error("!" * 60)
        return None
    
    # Step 5: Display system status
    logger.info("=" * 60)
    logger.info("Free AI System Ready!")
    logger.info(f"Active providers: {len(ai_manager.providers)}")
    logger.info(f"Provider priority: {ai_manager.provider_priority}")
    logger.info("=" * 60)
    
    return ai_manager


def get_ai_response(prompt: str, context: str = None) -> str:
    """
    Convenience function to get AI response
    
    Args:
        prompt: User prompt/question
        context: Optional system context
        
    Returns:
        AI generated response
    """
    import asyncio
    
    # Run async function in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(
            ai_manager.get_response(prompt, context)
        )
        return response
    finally:
        loop.close()


async def get_ai_response_async(prompt: str, context: str = None) -> str:
    """
    Async version of get_ai_response
    
    Args:
        prompt: User prompt/question
        context: Optional system context
        
    Returns:
        AI generated response
    """
    return await ai_manager.get_response(prompt, context)


def get_system_stats():
    """Get comprehensive system statistics"""
    stats = {
        'ai_manager': ai_manager.get_stats(),
        'cache': response_cache.get_stats(),
        'providers': ai_manager.get_provider_status()
    }
    
    return stats


def print_system_status():
    """Print formatted system status"""
    stats = get_system_stats()
    
    print("\n" + "=" * 60)
    print("FREE AI SYSTEM STATUS")
    print("=" * 60)
    
    # AI Manager stats
    print("\n📊 Overall Statistics:")
    print(f"  Total Requests: {stats['ai_manager']['total_requests']:,}")
    print(f"  Cache Hit Rate: {stats['ai_manager'].get('cache_hit_rate', 0):.1f}%")
    print(f"  Requests/Min: {stats['ai_manager'].get('requests_per_minute', 0):.1f}")
    
    # Cache stats
    print("\n💾 Cache Statistics:")
    print(f"  Backend: {stats['cache']['backend']}")
    print(f"  Hit Rate: {stats['cache']['hit_rate']:.1f}%")
    print(f"  Hits: {stats['cache']['hits']:,}")
    print(f"  Misses: {stats['cache']['misses']:,}")
    
    # Provider stats
    print("\n🤖 Provider Status:")
    for name, status in stats['providers'].items():
        available = "✓" if status['available'] else "✗"
        print(f"  {available} {name.capitalize()}: {status['requests_today']:,} requests today")
    
    # Provider-specific details
    if 'groq' in ai_manager.providers:
        groq_stats = ai_manager.providers['groq'].get_usage_stats()
        print(f"\n  Groq Details:")
        print(f"    Used: {groq_stats['total_used']:,} / {groq_stats['total_available']:,}")
        print(f"    Remaining: {groq_stats['remaining']:,}")
        print(f"    Usage: {groq_stats['usage_percentage']:.1f}%")
    
    print("\n" + "=" * 60 + "\n")


# Initialize on module import
logger.info("Loading free AI system module...")
