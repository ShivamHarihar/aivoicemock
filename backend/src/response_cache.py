"""
Response Cache - Intelligent caching system for AI responses
Uses in-memory cache with optional Redis backend for distributed caching
"""

import hashlib
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from collections import OrderedDict

logger = logging.getLogger(__name__)


class ResponseCache:
    """
    Intelligent caching system for AI responses.
    Supports both in-memory and Redis backends.
    """
    
    def __init__(self, backend='memory', ttl=86400, max_size=10000):
        """
        Initialize response cache
        
        Args:
            backend: 'memory' or 'redis'
            ttl: Time to live in seconds (default: 24 hours)
            max_size: Maximum cache size for memory backend
        """
        self.backend = backend
        self.ttl = ttl
        self.max_size = max_size
        
        if backend == 'redis':
            try:
                import redis
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                logger.info("Redis cache backend initialized")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Falling back to memory cache")
                self.backend = 'memory'
        
        if self.backend == 'memory':
            self.memory_cache = OrderedDict()
            logger.info(f"Memory cache initialized (max_size={max_size}, ttl={ttl}s)")
        
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'evictions': 0
        }
    
    def generate_key(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate cache key from prompt and context
        
        Args:
            prompt: The AI prompt
            context: Optional context
            
        Returns:
            MD5 hash of normalized prompt+context
        """
        # Normalize inputs
        normalized_prompt = prompt.strip().lower()
        normalized_context = context.strip().lower() if context else ''
        
        # Create deterministic key
        data = {
            'prompt': normalized_prompt,
            'context': normalized_context
        }
        key_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[str]:
        """
        Retrieve cached response
        
        Args:
            key: Cache key
            
        Returns:
            Cached response or None if not found/expired
        """
        try:
            if self.backend == 'redis':
                return self._get_redis(key)
            else:
                return self._get_memory(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, response: str):
        """
        Store response in cache
        
        Args:
            key: Cache key
            response: AI response to cache
        """
        try:
            if self.backend == 'redis':
                self._set_redis(key, response)
            else:
                self._set_memory(key, response)
            
            self.stats['sets'] += 1
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def _get_redis(self, key: str) -> Optional[str]:
        """Get from Redis cache"""
        cached = self.redis_client.get(f"ai_response:{key}")
        
        if cached:
            self.stats['hits'] += 1
            data = json.loads(cached)
            
            # Check expiration
            if datetime.fromisoformat(data['expires_at']) > datetime.now():
                return data['response']
            else:
                # Expired, delete it
                self.redis_client.delete(f"ai_response:{key}")
        
        self.stats['misses'] += 1
        return None
    
    def _set_redis(self, key: str, response: str):
        """Set in Redis cache"""
        data = {
            'response': response,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        }
        
        self.redis_client.setex(
            f"ai_response:{key}",
            self.ttl,
            json.dumps(data)
        )
    
    def _get_memory(self, key: str) -> Optional[str]:
        """Get from memory cache"""
        if key in self.memory_cache:
            data = self.memory_cache[key]
            
            # Check expiration
            if datetime.fromisoformat(data['expires_at']) > datetime.now():
                # Move to end (LRU)
                self.memory_cache.move_to_end(key)
                self.stats['hits'] += 1
                return data['response']
            else:
                # Expired, delete it
                del self.memory_cache[key]
        
        self.stats['misses'] += 1
        return None
    
    def _set_memory(self, key: str, response: str):
        """Set in memory cache"""
        # Check if we need to evict
        if len(self.memory_cache) >= self.max_size:
            # Remove oldest item (FIFO)
            self.memory_cache.popitem(last=False)
            self.stats['evictions'] += 1
        
        self.memory_cache[key] = {
            'response': response,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        }
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate percentage"""
        total = self.stats['hits'] + self.stats['misses']
        return (self.stats['hits'] / total * 100) if total > 0 else 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            **self.stats,
            'hit_rate': round(self.get_hit_rate(), 2),
            'size': len(self.memory_cache) if self.backend == 'memory' else 'N/A',
            'backend': self.backend
        }
    
    def clear(self):
        """Clear all cached items"""
        if self.backend == 'redis':
            # Delete all keys matching pattern
            for key in self.redis_client.scan_iter("ai_response:*"):
                self.redis_client.delete(key)
        else:
            self.memory_cache.clear()
        
        logger.info("Cache cleared")
    
    def cleanup_expired(self):
        """Remove expired items (for memory backend)"""
        if self.backend == 'memory':
            now = datetime.now()
            expired_keys = [
                key for key, data in self.memory_cache.items()
                if datetime.fromisoformat(data['expires_at']) <= now
            ]
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# Singleton instance
response_cache = ResponseCache(backend='memory', ttl=86400, max_size=10000)
