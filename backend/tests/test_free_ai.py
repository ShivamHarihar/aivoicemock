"""
Unit Tests for Free AI System
Tests for CI/CD pipeline
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.src.ai_provider_manager import AIProviderManager, UsageTracker, BaseAIProvider
from backend.src.response_cache import ResponseCache


class TestUsageTracker:
    """Test usage tracking functionality"""
    
    def test_initialization(self):
        """Test tracker initializes correctly"""
        tracker = UsageTracker()
        assert tracker.stats['total_requests'] == 0
        assert tracker.stats['cache_hits'] == 0
        assert tracker.stats['cache_misses'] == 0
    
    def test_log_request(self):
        """Test logging requests"""
        tracker = UsageTracker()
        tracker.log_request('test_provider', success=True)
        
        assert tracker.stats['total_requests'] == 1
        assert tracker.stats['provider_requests']['test_provider'] == 1
        assert tracker.stats['provider_failures']['test_provider'] == 0
    
    def test_log_failure(self):
        """Test logging failures"""
        tracker = UsageTracker()
        tracker.log_request('test_provider', success=False)
        
        assert tracker.stats['provider_failures']['test_provider'] == 1
    
    def test_cache_tracking(self):
        """Test cache hit/miss tracking"""
        tracker = UsageTracker()
        tracker.log_cache_hit()
        tracker.log_cache_hit()
        tracker.log_cache_miss()
        
        stats = tracker.get_stats()
        assert stats['cache_hits'] == 2
        assert stats['cache_misses'] == 1
        assert stats['cache_hit_rate'] == 66.67


class TestResponseCache:
    """Test caching functionality"""
    
    def test_cache_initialization(self):
        """Test cache initializes correctly"""
        cache = ResponseCache(backend='memory', ttl=3600, max_size=100)
        assert cache.backend == 'memory'
        assert cache.ttl == 3600
        assert cache.max_size == 100
    
    def test_generate_key(self):
        """Test cache key generation"""
        cache = ResponseCache(backend='memory')
        
        key1 = cache.generate_key("test prompt", "test context")
        key2 = cache.generate_key("test prompt", "test context")
        key3 = cache.generate_key("different prompt", "test context")
        
        assert key1 == key2  # Same input = same key
        assert key1 != key3  # Different input = different key
    
    def test_set_and_get(self):
        """Test setting and getting from cache"""
        cache = ResponseCache(backend='memory')
        
        cache.set("test_key", "test_response")
        result = cache.get("test_key")
        
        assert result == "test_response"
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = ResponseCache(backend='memory')
        result = cache.get("nonexistent_key")
        
        assert result is None
    
    def test_hit_rate_calculation(self):
        """Test hit rate calculation"""
        cache = ResponseCache(backend='memory')
        
        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        cache.get("key1")  # Hit
        
        hit_rate = cache.get_hit_rate()
        assert hit_rate == 66.67  # 2 hits out of 3 total


class TestAIProviderManager:
    """Test AI provider manager"""
    
    def test_initialization(self):
        """Test manager initializes correctly"""
        manager = AIProviderManager()
        
        assert manager.providers == {}
        assert isinstance(manager.usage_tracker, UsageTracker)
        assert manager.provider_priority == [
            'huggingface', 'groq', 'gemini', 'together', 'local'
        ]
    
    def test_register_provider(self):
        """Test provider registration"""
        manager = AIProviderManager()
        mock_provider = Mock(spec=BaseAIProvider)
        
        manager.register_provider('test_provider', mock_provider)
        
        assert 'test_provider' in manager.providers
        assert manager.providers['test_provider'] == mock_provider
    
    def test_set_cache(self):
        """Test cache configuration"""
        manager = AIProviderManager()
        mock_cache = Mock(spec=ResponseCache)
        
        manager.set_cache(mock_cache)
        
        assert manager.cache == mock_cache
    
    @pytest.mark.asyncio
    async def test_get_response_with_cache_hit(self):
        """Test response retrieval with cache hit"""
        manager = AIProviderManager()
        mock_cache = Mock(spec=ResponseCache)
        mock_cache.get.return_value = "cached_response"
        
        manager.set_cache(mock_cache)
        
        response = await manager.get_response("test prompt")
        
        assert response == "cached_response"
        mock_cache.get.assert_called_once()


class TestBaseAIProvider:
    """Test base provider functionality"""
    
    def test_initialization(self):
        """Test provider initializes correctly"""
        provider = BaseAIProvider("test_provider")
        
        assert provider.name == "test_provider"
        assert provider.request_count == 0
        assert provider.daily_limit is None
    
    def test_has_quota_unlimited(self):
        """Test quota check with unlimited quota"""
        provider = BaseAIProvider("test_provider")
        
        assert provider.has_quota() is True
    
    def test_has_quota_with_limit(self):
        """Test quota check with limit"""
        provider = BaseAIProvider("test_provider")
        provider.daily_limit = 100
        provider.request_count = 50
        
        assert provider.has_quota() is True
        
        provider.request_count = 100
        assert provider.has_quota() is False
    
    def test_reset_usage(self):
        """Test usage counter reset"""
        provider = BaseAIProvider("test_provider")
        provider.request_count = 50
        
        provider.reset_usage()
        
        assert provider.request_count == 0


# Integration Tests
class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.mark.asyncio
    async def test_full_request_flow(self):
        """Test complete request flow with cache"""
        manager = AIProviderManager()
        cache = ResponseCache(backend='memory')
        manager.set_cache(cache)
        
        # Create mock provider
        mock_provider = Mock(spec=BaseAIProvider)
        mock_provider.has_quota.return_value = True
        mock_provider.generate = Mock(return_value="test_response")
        
        # Make async
        async def async_generate(*args, **kwargs):
            return "test_response"
        
        mock_provider.generate = async_generate
        
        manager.register_provider('test', mock_provider)
        manager.provider_priority = ['test']
        
        # First request - should call provider
        response1 = await manager.get_response("test prompt")
        assert response1 == "test_response"
        
        # Second request - should hit cache
        response2 = await manager.get_response("test prompt")
        assert response2 == "test_response"
        
        # Check cache stats
        stats = manager.get_stats()
        assert stats['cache_hits'] == 1
        assert stats['cache_misses'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
