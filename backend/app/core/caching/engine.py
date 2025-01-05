"""
Caching Engine
PGF Protocol: CACHE_001
Gate: GATE_6
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, TypeVar, Generic
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import json
import hashlib
import asyncio
import aioredis
from functools import wraps
import pickle

T = TypeVar("T")

class CacheBackend(str, Enum):
    """Cache backend types"""
    MEMORY = "memory"
    REDIS = "redis"
    FILE = "file"

class CacheStrategy(str, Enum):
    """Cache strategies"""
    LRU = "lru"      # Least Recently Used
    LFU = "lfu"      # Least Frequently Used
    FIFO = "fifo"    # First In First Out
    TTL = "ttl"      # Time To Live

class CacheConfig(BaseModel):
    """Cache configuration"""
    
    backend: CacheBackend
    strategy: CacheStrategy
    ttl: int = 300  # seconds
    max_size: int = 1000  # items
    connection_url: Optional[str] = None
    namespace: str = "kundli"
    options: Dict[str, Any] = Field(default_factory=dict)

class CacheEntry(BaseModel, Generic[T]):
    """Cache entry"""
    
    key: str
    value: T
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    ttl: int
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CacheEngine:
    """Caching engine for data caching"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self._cache: Dict[str, CacheEntry] = {}
        self._redis = None
        self._initialized = False
        self._lock = asyncio.Lock()
    
    async def initialize(self) -> None:
        """Initialize cache engine"""
        if self._initialized:
            return
            
        if self.config.backend == CacheBackend.REDIS:
            self._redis = await aioredis.create_redis_pool(self.config.connection_url)
            
        self._initialized = True
    
    async def close(self) -> None:
        """Close cache engine connections"""
        if self.config.backend == CacheBackend.REDIS and self._redis:
            self._redis.close()
            await self._redis.wait_closed()
    
    def _build_key(self, key: str) -> str:
        """Build cache key with namespace"""
        return f"{self.config.namespace}:{key}"
    
    def _serialize(self, value: Any) -> bytes:
        """Serialize value for storage"""
        return pickle.dumps(value)
    
    def _deserialize(self, value: bytes) -> Any:
        """Deserialize value from storage"""
        return pickle.loads(value)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._initialized:
            await self.initialize()
            
        full_key = self._build_key(key)
        
        if self.config.backend == CacheBackend.MEMORY:
            async with self._lock:
                entry = self._cache.get(full_key)
                if not entry:
                    return None
                    
                # Check TTL
                if (datetime.utcnow() - entry.created_at).total_seconds() > entry.ttl:
                    del self._cache[full_key]
                    return None
                    
                # Update access stats
                entry.accessed_at = datetime.utcnow()
                entry.access_count += 1
                return entry.value
                
        elif self.config.backend == CacheBackend.REDIS:
            value = await self._redis.get(full_key)
            if value:
                return self._deserialize(value)
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Set value in cache"""
        if not self._initialized:
            await self.initialize()
            
        full_key = self._build_key(key)
        now = datetime.utcnow()
        
        if self.config.backend == CacheBackend.MEMORY:
            async with self._lock:
                # Apply cache strategy if max size reached
                if len(self._cache) >= self.config.max_size:
                    await self._apply_cache_strategy()
                
                self._cache[full_key] = CacheEntry(
                    key=full_key,
                    value=value,
                    created_at=now,
                    accessed_at=now,
                    ttl=ttl or self.config.ttl,
                    metadata=metadata or {}
                )
                
        elif self.config.backend == CacheBackend.REDIS:
            await self._redis.set(
                full_key,
                self._serialize(value),
                expire=ttl or self.config.ttl
            )
    
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if not self._initialized:
            await self.initialize()
            
        full_key = self._build_key(key)
        
        if self.config.backend == CacheBackend.MEMORY:
            async with self._lock:
                self._cache.pop(full_key, None)
                
        elif self.config.backend == CacheBackend.REDIS:
            await self._redis.delete(full_key)
    
    async def clear(self) -> None:
        """Clear all values from cache"""
        if not self._initialized:
            await self.initialize()
            
        if self.config.backend == CacheBackend.MEMORY:
            async with self._lock:
                self._cache.clear()
                
        elif self.config.backend == CacheBackend.REDIS:
            await self._redis.flushdb()
    
    async def _apply_cache_strategy(self) -> None:
        """Apply cache eviction strategy"""
        if self.config.strategy == CacheStrategy.LRU:
            # Remove least recently used entry
            lru_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].accessed_at
            )
            del self._cache[lru_key]
            
        elif self.config.strategy == CacheStrategy.LFU:
            # Remove least frequently used entry
            lfu_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].access_count
            )
            del self._cache[lfu_key]
            
        elif self.config.strategy == CacheStrategy.FIFO:
            # Remove oldest entry
            fifo_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].created_at
            )
            del self._cache[fifo_key]
            
        elif self.config.strategy == CacheStrategy.TTL:
            # Remove expired entries
            now = datetime.utcnow()
            expired = [
                k for k, v in self._cache.items()
                if (now - v.created_at).total_seconds() > v.ttl
            ]
            for key in expired:
                del self._cache[key]

def cached(
    ttl: Optional[int] = None,
    key_builder: Optional[callable] = None
):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default key builder using function name and arguments
                key_parts = [func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            cached_value = await cache_engine.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_engine.set(cache_key, result, ttl=ttl)
            return result
            
        return wrapper
    return decorator

# Global cache engine instance
cache_engine = CacheEngine(
    CacheConfig(
        backend=CacheBackend.MEMORY,
        strategy=CacheStrategy.LRU,
        ttl=300,
        max_size=1000,
        namespace="kundli"
    )
)
