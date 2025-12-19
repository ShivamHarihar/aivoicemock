"""
AI Provider Manager - Multi-Provider Load Balancer for Free AI Services
Handles intelligent routing across multiple free AI providers with caching and fallback
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


class AIProviderManager:
    """
    Manages multiple AI providers with intelligent load balancing and caching.
    Supports: HuggingFace, Groq, Gemini, Together AI, and Local LLM
    """
    
    def __init__(self):
        self.providers = {}
        self.usage_tracker = UsageTracker()
        self.cache = None  # Will be initialized with ResponseCache
        self.provider_priority = [
            'huggingface',
            'groq', 
            'gemini',
            'together',
            'local'
        ]
        
        logger.info("AI Provider Manager initialized")
    
    def register_provider(self, name: str, provider):
        """Register a new AI provider"""
        self.providers[name] = provider
        logger.info(f"Registered provider: {name}")
    
    def set_cache(self, cache):
        """Set the response cache instance"""
        self.cache = cache
    
    async def get_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Get AI response with intelligent provider selection and caching
        
        Args:
            prompt: The user prompt/question
            context: Optional system context
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0-1)
            
        Returns:
            AI generated response text
        """
        
        # Check cache first
        if self.cache:
            cache_key = self._generate_cache_key(prompt, context)
            if cached_response := self.cache.get(cache_key):
                logger.info(f"Cache hit for prompt: {prompt[:50]}...")
                self.usage_tracker.log_cache_hit()
                return cached_response
            
            self.usage_tracker.log_cache_miss()
        
        # Try providers in priority order
        last_error = None
        
        for provider_name in self.provider_priority:
            if provider_name not in self.providers:
                continue
            
            provider = self.providers[provider_name]
            
            # Check if provider has available quota
            if not provider.has_quota():
                logger.warning(f"Provider {provider_name} quota exhausted")
                continue
            
            try:
                logger.info(f"Attempting provider: {provider_name}")
                
                response = await provider.generate(
                    prompt=prompt,
                    context=context,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                # Log successful usage
                self.usage_tracker.log_request(provider_name, success=True)
                
                # Cache the response
                if self.cache:
                    self.cache.set(cache_key, response)
                
                logger.info(f"Success with provider: {provider_name}")
                return response
                
            except Exception as e:
                last_error = e
                logger.error(f"Provider {provider_name} failed: {str(e)}")
                self.usage_tracker.log_request(provider_name, success=False)
                
                # Continue to next provider
                continue
        
        # All providers failed
        error_msg = f"All AI providers exhausted. Last error: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def _generate_cache_key(self, prompt: str, context: Optional[str]) -> str:
        """Generate cache key from prompt and context"""
        data = {
            'prompt': prompt.strip().lower(),
            'context': context.strip().lower() if context else ''
        }
        key_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics across all providers"""
        return self.usage_tracker.get_stats()
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered providers"""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                'available': provider.has_quota(),
                'requests_today': provider.get_usage_count() if hasattr(provider, 'get_usage_count') else 0
            }
        return status


class UsageTracker:
    """Track usage statistics across all providers"""
    
    def __init__(self):
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'provider_requests': {},
            'provider_failures': {},
            'start_time': datetime.now()
        }
    
    def log_request(self, provider: str, success: bool = True):
        """Log a provider request"""
        self.stats['total_requests'] += 1
        
        if provider not in self.stats['provider_requests']:
            self.stats['provider_requests'][provider] = 0
            self.stats['provider_failures'][provider] = 0
        
        self.stats['provider_requests'][provider] += 1
        
        if not success:
            self.stats['provider_failures'][provider] += 1
    
    def log_cache_hit(self):
        """Log a cache hit"""
        self.stats['cache_hits'] += 1
    
    def log_cache_miss(self):
        """Log a cache miss"""
        self.stats['cache_misses'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        total_cache_requests = self.stats['cache_hits'] + self.stats['cache_misses']
        cache_hit_rate = (
            (self.stats['cache_hits'] / total_cache_requests * 100)
            if total_cache_requests > 0 else 0
        )
        
        runtime = (datetime.now() - self.stats['start_time']).total_seconds()
        requests_per_minute = (
            (self.stats['total_requests'] / runtime * 60)
            if runtime > 0 else 0
        )
        
        return {
            **self.stats,
            'cache_hit_rate': round(cache_hit_rate, 2),
            'requests_per_minute': round(requests_per_minute, 2),
            'runtime_seconds': round(runtime, 2)
        }
    
    def reset(self):
        """Reset all statistics"""
        self.__init__()


class BaseAIProvider:
    """Base class for all AI providers"""
    
    def __init__(self, name: str):
        self.name = name
        self.request_count = 0
        self.daily_limit = None
    
    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate AI response - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement generate()")
    
    def has_quota(self) -> bool:
        """Check if provider has available quota"""
        if self.daily_limit is None:
            return True
        return self.request_count < self.daily_limit
    
    def get_usage_count(self) -> int:
        """Get current usage count"""
        return self.request_count
    
    def reset_usage(self):
        """Reset usage counter (call daily)"""
        self.request_count = 0
        logger.info(f"Reset usage counter for {self.name}")


# Singleton instance
ai_manager = AIProviderManager()
