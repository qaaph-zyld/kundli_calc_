"""
Cache Manager for Knowledge Engine
====================================

Provides caching layer for interpretation queries to improve performance.
Uses in-memory caching with LRU (Least Recently Used) eviction.

Performance targets:
- Cached queries: <0.001s (1ms)
- Cache hit rate: >80% for repeated queries
- Memory footprint: <50MB for 1000 cached interpretations
"""

from typing import Dict, Any, Optional, Tuple
from functools import lru_cache
from datetime import datetime
import hashlib
import json


class InterpretationCache:
    """
    LRU cache for planet-in-house interpretations.
    
    Caches both single-source and multi-source interpretations
    to minimize repeated lookups and comparisons.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize cache with maximum size.
        
        Args:
            max_size: Maximum number of cached entries (default 1000)
        """
        self.max_size = max_size
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_counts: Dict[str, int] = {}
        self.last_accessed: Dict[str, datetime] = {}
        self.hits = 0
        self.misses = 0
    
    def _generate_key(
        self,
        planet: str,
        house: int,
        sign: str = "",
        dignity: str = "",
        multi_source: bool = False
    ) -> str:
        """
        Generate cache key for query.
        
        Args:
            planet: Planet name
            house: House number
            sign: Sign name (optional)
            dignity: Dignity (optional)
            multi_source: Whether this is multi-source query
            
        Returns:
            Hash-based cache key
        """
        key_data = {
            'planet': planet,
            'house': house,
            'sign': sign,
            'dignity': dignity,
            'multi_source': multi_source
        }
        
        # Create consistent JSON string
        key_string = json.dumps(key_data, sort_keys=True)
        
        # Generate hash for compact key
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(
        self,
        planet: str,
        house: int,
        sign: str = "",
        dignity: str = "",
        multi_source: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached interpretation if available.
        
        Returns:
            Cached interpretation or None if not found
        """
        key = self._generate_key(planet, house, sign, dignity, multi_source)
        
        if key in self.cache:
            self.hits += 1
            self.access_counts[key] = self.access_counts.get(key, 0) + 1
            self.last_accessed[key] = datetime.now()
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def set(
        self,
        planet: str,
        house: int,
        interpretation: Dict[str, Any],
        sign: str = "",
        dignity: str = "",
        multi_source: bool = False
    ) -> None:
        """
        Cache an interpretation.
        
        Args:
            planet: Planet name
            house: House number
            interpretation: Interpretation data to cache
            sign: Sign name (optional)
            dignity: Dignity (optional)
            multi_source: Whether this is multi-source
        """
        key = self._generate_key(planet, house, sign, dignity, multi_source)
        
        # Evict if cache is full
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_lru()
        
        self.cache[key] = interpretation
        self.access_counts[key] = 1
        self.last_accessed[key] = datetime.now()
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry"""
        if not self.last_accessed:
            return
        
        # Find least recently accessed
        lru_key = min(self.last_accessed.items(), key=lambda x: x[1])[0]
        
        # Remove from all dictionaries
        del self.cache[lru_key]
        del self.access_counts[lru_key]
        del self.last_accessed[lru_key]
    
    def clear(self) -> None:
        """Clear all cached entries"""
        self.cache.clear()
        self.access_counts.clear()
        self.last_accessed.clear()
        self.hits = 0
        self.misses = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache performance metrics
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total_requests,
            'hit_rate_percent': round(hit_rate, 2),
            'most_accessed': self._get_most_accessed(5)
        }
    
    def _get_most_accessed(self, limit: int = 5) -> list:
        """Get most frequently accessed entries"""
        sorted_access = sorted(
            self.access_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [
            {'key': key[:8], 'access_count': count}
            for key, count in sorted_access[:limit]
        ]


# Global cache instance
_interpretation_cache = InterpretationCache(max_size=1000)


def get_cache() -> InterpretationCache:
    """Get global cache instance"""
    return _interpretation_cache


# Decorator for caching function results
def cache_interpretation(func):
    """
    Decorator to cache interpretation function results.
    
    Usage:
        @cache_interpretation
        def get_interpretation(planet, house):
            # ... expensive computation
            return interpretation
    """
    def wrapper(planet: str, house: int, *args, **kwargs):
        cache = get_cache()
        
        # Try to get from cache
        cached = cache.get(planet, house)
        if cached is not None:
            return cached
        
        # Compute if not cached
        result = func(planet, house, *args, **kwargs)
        
        # Cache the result
        cache.set(planet, house, result)
        
        return result
    
    return wrapper


# Performance monitoring
class PerformanceMonitor:
    """Monitor performance metrics for interpretation operations"""
    
    def __init__(self):
        self.operation_times: Dict[str, list] = {}
        self.operation_counts: Dict[str, int] = {}
    
    def record(self, operation: str, duration: float) -> None:
        """Record operation timing"""
        if operation not in self.operation_times:
            self.operation_times[operation] = []
            self.operation_counts[operation] = 0
        
        self.operation_times[operation].append(duration)
        self.operation_counts[operation] += 1
        
        # Keep only last 100 times to avoid memory growth
        if len(self.operation_times[operation]) > 100:
            self.operation_times[operation] = self.operation_times[operation][-100:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics"""
        stats = {}
        
        for operation, times in self.operation_times.items():
            if times:
                stats[operation] = {
                    'count': self.operation_counts[operation],
                    'avg_ms': round(sum(times) / len(times) * 1000, 2),
                    'min_ms': round(min(times) * 1000, 2),
                    'max_ms': round(max(times) * 1000, 2),
                    'recent_avg_ms': round(sum(times[-10:]) / len(times[-10:]) * 1000, 2) if len(times) >= 10 else round(sum(times) / len(times) * 1000, 2)
                }
        
        return stats
    
    def reset(self) -> None:
        """Reset all statistics"""
        self.operation_times.clear()
        self.operation_counts.clear()


# Global performance monitor
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    return _performance_monitor
