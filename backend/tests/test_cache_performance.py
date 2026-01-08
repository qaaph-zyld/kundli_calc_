"""Tests for caching and performance optimization"""
import pytest
from backend.app.core.knowledge.engine.cache_manager import (
    InterpretationCache, get_cache, PerformanceMonitor
)

class TestCaching:
    def test_cache_basic(self):
        cache = InterpretationCache(max_size=100)
        cache.set('Sun', 1, {'data': 'test'})
        result = cache.get('Sun', 1)
        assert result == {'data': 'test'}
        assert cache.hits == 1
    
    def test_cache_statistics(self):
        cache = InterpretationCache()
        cache.set('Sun', 1, {'test': 1})
        cache.get('Sun', 1)
        stats = cache.get_statistics()
        assert stats['hit_rate_percent'] > 0
