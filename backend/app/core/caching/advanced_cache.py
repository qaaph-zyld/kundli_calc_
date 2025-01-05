"""
Advanced Caching System
PGF Protocol: CACHE_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, TypeVar, Generic, Callable
from dataclasses import dataclass
import asyncio
import logging
import time
import json
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from collections import OrderedDict
import threading
import weakref

T = TypeVar('T')

@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    memory_usage: float = 0.0
    avg_access_time: float = 0.0
    cache_size: int = 0

class CacheItem(Generic[T]):
    """Represents a cached item with metadata"""
    def __init__(
        self,
        key: str,
        value: T,
        expiry: Optional[datetime] = None,
        cost: float = 1.0
    ):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.cost = cost
        self.last_access = datetime.now()
        self.access_count = 0
        self.creation_time = datetime.now()

class AdvancedCache(Generic[T]):
    """Advanced caching system with multiple eviction policies"""
    
    def __init__(
        self,
        max_size: int = 1000,
        max_memory_mb: float = 100.0,
        default_ttl: int = 3600,
        eviction_policy: str = "adaptive"
    ):
        self.max_size = max_size
        self.max_memory_mb = max_memory_mb
        self.default_ttl = default_ttl
        self.eviction_policy = eviction_policy
        self.cache: OrderedDict[str, CacheItem[T]] = OrderedDict()
        self.metrics = CacheMetrics()
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Start background tasks
        self._start_maintenance_tasks()
    
    def _start_maintenance_tasks(self) -> None:
        """Start background maintenance tasks"""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        self._metrics_task = asyncio.create_task(self._update_metrics())
    
    async def _periodic_cleanup(self) -> None:
        """Periodically clean up expired items"""
        while True:
            try:
                await asyncio.sleep(60)  # Run every minute
                await self.cleanup_expired()
            except Exception as e:
                self.logger.error(f"Cleanup task error: {str(e)}")
    
    async def _update_metrics(self) -> None:
        """Periodically update cache metrics"""
        while True:
            try:
                await asyncio.sleep(30)  # Run every 30 seconds
                self.metrics.memory_usage = self._calculate_memory_usage()
                self.metrics.cache_size = len(self.cache)
            except Exception as e:
                self.logger.error(f"Metrics update error: {str(e)}")
    
    def _calculate_key(self, value: Any) -> str:
        """Calculate cache key for a value"""
        if isinstance(value, (str, int, float, bool)):
            return str(value)
        return hashlib.sha256(
            json.dumps(value, sort_keys=True).encode()
        ).hexdigest()
    
    def _calculate_memory_usage(self) -> float:
        """Calculate current memory usage in MB"""
        import sys
        total_size = sum(
            sys.getsizeof(item.value) for item in self.cache.values()
        )
        return total_size / (1024 * 1024)
    
    async def get(self, key: str) -> Optional[T]:
        """Get value from cache"""
        start_time = time.time()
        
        with self.lock:
            item = self.cache.get(key)
            
            if item is None:
                self.metrics.misses += 1
                return None
            
            if item.expiry and datetime.now() > item.expiry:
                self.metrics.misses += 1
                del self.cache[key]
                return None
            
            # Update access metrics
            item.last_access = datetime.now()
            item.access_count += 1
            self.metrics.hits += 1
            
            # Update average access time
            self.metrics.avg_access_time = (
                (self.metrics.avg_access_time * (self.metrics.hits - 1) +
                 (time.time() - start_time)) / self.metrics.hits
            )
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            
            return item.value
    
    async def put(
        self,
        key: str,
        value: T,
        ttl: Optional[int] = None,
        cost: float = 1.0
    ) -> bool:
        """Put value in cache"""
        with self.lock:
            # Check memory limit
            if self._calculate_memory_usage() >= self.max_memory_mb:
                await self._evict()
            
            # Calculate expiry
            expiry = (
                datetime.now() + timedelta(seconds=ttl)
                if ttl else
                datetime.now() + timedelta(seconds=self.default_ttl)
            )
            
            # Create cache item
            item = CacheItem(key, value, expiry, cost)
            
            # Add to cache
            self.cache[key] = item
            
            # Check size limit
            if len(self.cache) > self.max_size:
                await self._evict()
            
            return True
    
    async def _evict(self) -> None:
        """Evict items based on policy"""
        if not self.cache:
            return
        
        if self.eviction_policy == "lru":
            # Least Recently Used
            self.cache.popitem(last=False)
        elif self.eviction_policy == "cost":
            # Highest Cost
            max_cost_key = max(
                self.cache.items(),
                key=lambda x: x[1].cost
            )[0]
            del self.cache[max_cost_key]
        else:  # adaptive
            # Consider multiple factors
            scores = {
                key: self._calculate_item_score(item)
                for key, item in self.cache.items()
            }
            worst_key = min(scores.items(), key=lambda x: x[1])[0]
            del self.cache[worst_key]
        
        self.metrics.evictions += 1
    
    def _calculate_item_score(self, item: CacheItem[T]) -> float:
        """Calculate item score for adaptive eviction"""
        age = (datetime.now() - item.creation_time).total_seconds()
        time_since_access = (
            datetime.now() - item.last_access
        ).total_seconds()
        
        # Normalize factors
        age_factor = 1 / (1 + age / 3600)  # Age in hours
        access_factor = item.access_count / (1 + time_since_access / 3600)
        cost_factor = 1 / (1 + item.cost)
        
        # Weighted score
        return (0.4 * access_factor + 0.3 * age_factor + 0.3 * cost_factor)
    
    async def cleanup_expired(self) -> int:
        """Clean up expired items"""
        with self.lock:
            current_time = datetime.now()
            expired_keys = [
                key for key, item in self.cache.items()
                if item.expiry and current_time > item.expiry
            ]
            
            for key in expired_keys:
                del self.cache[key]
                self.metrics.evictions += 1
            
            return len(expired_keys)
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get current cache metrics"""
        return {
            "hits": self.metrics.hits,
            "misses": self.metrics.misses,
            "hit_ratio": (
                self.metrics.hits /
                (self.metrics.hits + self.metrics.misses)
                if (self.metrics.hits + self.metrics.misses) > 0
                else 0
            ),
            "evictions": self.metrics.evictions,
            "memory_usage_mb": self.metrics.memory_usage,
            "avg_access_time": self.metrics.avg_access_time,
            "cache_size": self.metrics.cache_size
        }
    
    async def clear(self) -> None:
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            self.metrics = CacheMetrics()

def cached(
    cache: AdvancedCache,
    ttl: Optional[int] = None,
    cost: float = 1.0
):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Calculate cache key
            key_data = {
                'func': func.__name__,
                'args': args,
                'kwargs': kwargs
            }
            key = cache._calculate_key(key_data)
            
            # Try to get from cache
            result = await cache.get(key)
            if result is not None:
                return result
            
            # Calculate result
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache.put(key, result, ttl, cost)
            
            return result
        return wrapper
    return decorator
