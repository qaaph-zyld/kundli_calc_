"""
Enhanced Redis Cache Implementation
Implements caching strategies and patterns for the Kundli Calculation Service
"""
from typing import Optional, Any, Union, List, Dict
from datetime import datetime, timedelta
import json
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    """Enhanced Redis cache implementation with advanced features"""
    
    def __init__(self):
        self._pool = None
        self._redis = None
        self._initialized = False
        self._fallback_mode = os.environ.get("ENV") == "test"
        self._memory_cache: Dict[str, Any] = {}
    
    def _init_redis(self):
        """Lazy initialization of Redis connection"""
        if self._initialized:
            return
        
        if self._fallback_mode:
            logger.info("Running in test/fallback mode - using in-memory cache")
            self._initialized = True
            return
            
        try:
            from redis import Redis, ConnectionPool
            from app.core.config.settings import settings
            
            self._pool = ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                username=settings.REDIS_USERNAME,
                password=settings.REDIS_PASSWORD,
                ssl=settings.REDIS_SSL,
                decode_responses=True,
                socket_timeout=settings.REDIS_TIMEOUT
            )
            self._redis = Redis(connection_pool=self._pool)
            self._redis.ping()  # Test connection
            self._initialized = True
        except Exception as e:
            logger.warning(f"Redis connection failed, using fallback in-memory cache: {e}")
            self._fallback_mode = True
            self._initialized = True
    
    @property
    def redis(self):
        """Get Redis client with lazy initialization"""
        self._init_redis()
        return self._redis
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with automatic deserialization"""
        self._init_redis()
        if self._fallback_mode:
            return self._memory_cache.get(key)
        try:
            value = self._redis.get(key)
            if value is None:
                return None
            return json.loads(value)
        except (json.JSONDecodeError, pickle.UnpicklingError, AttributeError):
            return None
            
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """Set value in cache with automatic serialization"""
        self._init_redis()
        if self._fallback_mode:
            self._memory_cache[key] = value
            return True
        try:
            serialized = json.dumps(value)
            return bool(
                self._redis.set(
                    key,
                    serialized,
                    ex=expire,
                    nx=nx,
                    xx=xx
                )
            )
        except (TypeError, json.JSONEncodeError, AttributeError):
            return False
            
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        self._init_redis()
        if self._fallback_mode:
            return self._memory_cache.pop(key, None) is not None
        try:
            return bool(self._redis.delete(key))
        except (AttributeError, Exception):
            return False
        
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        self._init_redis()
        if self._fallback_mode:
            return key in self._memory_cache
        try:
            return bool(self._redis.exists(key))
        except (AttributeError, Exception):
            return False
        
    async def incr(self, key: str) -> int:
        """Increment value"""
        self._init_redis()
        if self._fallback_mode:
            self._memory_cache[key] = self._memory_cache.get(key, 0) + 1
            return self._memory_cache[key]
        try:
            return self._redis.incr(key)
        except (AttributeError, Exception):
            return 0
        
    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration"""
        self._init_redis()
        if self._fallback_mode:
            return True  # No-op in memory mode
        try:
            return bool(self._redis.expire(key, seconds))
        except (AttributeError, Exception):
            return False
        
    async def ttl(self, key: str) -> int:
        """Get key time to live"""
        self._init_redis()
        if self._fallback_mode:
            return -1  # No TTL in memory mode
        try:
            return self._redis.ttl(key)
        except (AttributeError, Exception):
            return -1
        
    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern"""
        self._init_redis()
        if self._fallback_mode:
            import fnmatch
            return [k for k in self._memory_cache.keys() if fnmatch.fnmatch(k, pattern)]
        try:
            return self._redis.keys(pattern)
        except (AttributeError, Exception):
            return []
        
    async def flush(self) -> bool:
        """Flush all keys in current database"""
        self._init_redis()
        if self._fallback_mode:
            self._memory_cache.clear()
            return True
        try:
            return bool(self._redis.flushdb())
        except (AttributeError, Exception):
            return False
        
    async def hash_set(self, name: str, mapping: Dict[str, Any]) -> bool:
        """Set hash mapping"""
        self._init_redis()
        if self._fallback_mode:
            if name not in self._memory_cache:
                self._memory_cache[name] = {}
            self._memory_cache[name].update(mapping)
            return True
        try:
            serialized_mapping = {
                k: json.dumps(v)
                for k, v in mapping.items()
            }
            return bool(self._redis.hset(name, mapping=serialized_mapping))
        except (TypeError, json.JSONEncodeError, AttributeError):
            return False
            
    async def hash_get(self, name: str, key: str) -> Optional[Any]:
        """Get hash value"""
        self._init_redis()
        if self._fallback_mode:
            return self._memory_cache.get(name, {}).get(key)
        try:
            value = self._redis.hget(name, key)
            if value is None:
                return None
            return json.loads(value)
        except (json.JSONDecodeError, pickle.UnpicklingError, AttributeError):
            return None
            
    async def hash_getall(self, name: str) -> Dict[str, Any]:
        """Get all hash values"""
        self._init_redis()
        if self._fallback_mode:
            return self._memory_cache.get(name, {})
        try:
            mapping = self._redis.hgetall(name)
            return {
                k: json.loads(v)
                for k, v in mapping.items()
            }
        except (json.JSONDecodeError, pickle.UnpicklingError, AttributeError):
            return {}
            
    async def pipeline(self) -> 'RedisPipeline':
        """Get Redis pipeline"""
        self._init_redis()
        if self._fallback_mode:
            return MemoryPipeline(self._memory_cache)
        try:
            return RedisPipeline(self._redis.pipeline())
        except (AttributeError, Exception):
            return MemoryPipeline(self._memory_cache)
        

class MemoryPipeline:
    """In-memory pipeline for test/fallback mode"""
    
    def __init__(self, cache: Dict[str, Any]):
        self._cache = cache
        self._ops: List[tuple] = []
        
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        self._ops.append(('set', key, value))
        
    async def get(self, key: str):
        self._ops.append(('get', key))
        
    async def delete(self, key: str):
        self._ops.append(('delete', key))
        
    async def execute(self) -> List[Any]:
        results = []
        for op in self._ops:
            if op[0] == 'set':
                self._cache[op[1]] = op[2]
                results.append(True)
            elif op[0] == 'get':
                results.append(self._cache.get(op[1]))
            elif op[0] == 'delete':
                results.append(self._cache.pop(op[1], None) is not None)
        self._ops.clear()
        return results


class RedisPipeline:
    """Redis pipeline wrapper"""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """Add set command to pipeline"""
        try:
            serialized = json.dumps(value)
            self.pipeline.set(key, serialized, ex=expire)
        except (TypeError, json.JSONEncodeError):
            pass
            
    async def get(self, key: str):
        """Add get command to pipeline"""
        self.pipeline.get(key)
        
    async def delete(self, key: str):
        """Add delete command to pipeline"""
        self.pipeline.delete(key)
        
    async def execute(self) -> List[Any]:
        """Execute pipeline"""
        try:
            results = self.pipeline.execute()
            return [
                json.loads(result) if isinstance(result, str) else result
                for result in results
            ]
        except (json.JSONDecodeError, pickle.UnpicklingError):
            return results
            

# Global cache instance
cache = RedisCache()
