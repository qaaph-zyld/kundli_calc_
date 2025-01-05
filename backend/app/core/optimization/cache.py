"""
Caching Module
PGF Protocol: CACHE_001
Gate: GATE_4
Version: 1.0.0
"""

import json
import hashlib
from typing import Any, Optional, Dict, Union
from datetime import datetime, timedelta
import asyncio
from redis import asyncio as aioredis
from functools import wraps
import logging
from .profiler import cache_profiler

# Configure logging
logger = logging.getLogger(__name__)

class CacheConfig:
    """Cache configuration settings"""
    
    # TTL settings (in seconds)
    TTL = {
        'kundli': 3600,  # 1 hour
        'planetary': 7200,  # 2 hours
        'transit': 1800,  # 30 minutes
        'compatibility': 86400,  # 24 hours
        'default': 3600  # 1 hour default
    }
    
    # Maximum item sizes (in bytes)
    MAX_SIZES = {
        'kundli': 50_000,  # 50KB
        'planetary': 20_000,  # 20KB
        'transit': 10_000,  # 10KB
        'compatibility': 100_000,  # 100KB
        'default': 50_000  # 50KB default
    }
    
    # Cache prefixes
    PREFIXES = {
        'kundli': 'kdl:',
        'planetary': 'plt:',
        'transit': 'trn:',
        'compatibility': 'cmp:',
        'user': 'usr:'
    }

class AsyncCache:
    """Asynchronous caching implementation using Redis"""
    
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(
            redis_url,
            encoding='utf-8',
            decode_responses=True
        )
        self.config = CacheConfig()
    
    async def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_string = ":".join(key_parts)
        
        # Create hash of the key string
        key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
        
        return f"{self.config.PREFIXES.get(prefix, '')}{key_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = await self.redis.get(key)
            if value:
                cache_profiler.record_cache_result('get', True)
                return json.loads(value)
            cache_profiler.record_cache_result('get', False)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        max_size: Optional[int] = None
    ) -> bool:
        """Set value in cache"""
        try:
            # Serialize value
            serialized = json.dumps(value)
            
            # Check size
            size = len(serialized.encode('utf-8'))
            if max_size and size > max_size:
                logger.warning(f"Cache value too large: {size} bytes")
                return False
            
            # Set with TTL
            await self.redis.set(
                key,
                serialized,
                ex=ttl if ttl is not None else self.config.TTL['default']
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache clear pattern error: {str(e)}")
            return 0

def cached(
    prefix: str,
    ttl: Optional[int] = None,
    max_size: Optional[int] = None
):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Get cache instance
            cache = self.cache if hasattr(self, 'cache') else None
            if not cache or not isinstance(cache, AsyncCache):
                return await func(self, *args, **kwargs)
            
            # Generate cache key
            key = await cache._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Calculate result
            result = await func(self, *args, **kwargs)
            
            # Cache result
            if result is not None:
                await cache.set(
                    key,
                    result,
                    ttl=ttl or cache.config.TTL.get(prefix),
                    max_size=max_size or cache.config.MAX_SIZES.get(prefix)
                )
            
            return result
        
        return wrapper
    return decorator

class CacheManager:
    """Cache management utilities"""
    
    def __init__(self, cache: AsyncCache):
        self.cache = cache
    
    async def clear_user_cache(self, user_id: str) -> int:
        """Clear all cache entries for a user"""
        pattern = f"{self.cache.config.PREFIXES['user']}{user_id}:*"
        return await self.cache.clear_pattern(pattern)
    
    async def clear_kundli_cache(self, kundli_id: str) -> int:
        """Clear all cache entries for a kundli"""
        pattern = f"{self.cache.config.PREFIXES['kundli']}{kundli_id}:*"
        return await self.cache.clear_pattern(pattern)
    
    async def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        stats = {}
        for prefix in self.cache.config.PREFIXES.values():
            pattern = f"{prefix}*"
            keys = await self.cache.redis.keys(pattern)
            stats[prefix.rstrip(':')] = len(keys)
        return stats

# Usage examples:
"""
# Initialize cache
cache = AsyncCache(redis_url="redis://localhost:6379/0")
cache_manager = CacheManager(cache)

class KundliService:
    def __init__(self, cache: AsyncCache):
        self.cache = cache
    
    @cached('kundli')
    async def calculate_kundli(self, date: str, time: str, lat: float, lon: float):
        # Implementation
        pass
    
    @cached('planetary', ttl=7200)
    async def get_planetary_positions(self, date: str):
        # Implementation
        pass
"""
