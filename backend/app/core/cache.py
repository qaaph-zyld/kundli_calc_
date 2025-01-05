"""
Enhanced Redis Cache Implementation
Implements caching strategies and patterns for the Kundli Calculation Service
"""
from typing import Optional, Any, Union, List, Dict
from datetime import datetime, timedelta
import json
import pickle
from redis import Redis, ConnectionPool
from app.core.config.settings import settings

class RedisCache:
    """Enhanced Redis cache implementation with advanced features"""
    
    def __init__(self):
        self.pool = ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            ssl=settings.REDIS_SSL,
            decode_responses=True,
            socket_timeout=settings.REDIS_TIMEOUT
        )
        self.redis = Redis(connection_pool=self.pool)
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with automatic deserialization"""
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            return json.loads(value)
        except (json.JSONDecodeError, pickle.UnpicklingError):
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
        try:
            serialized = json.dumps(value)
            return bool(
                self.redis.set(
                    key,
                    serialized,
                    ex=expire,
                    nx=nx,
                    xx=xx
                )
            )
        except (TypeError, json.JSONEncodeError):
            return False
            
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        return bool(self.redis.delete(key))
        
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        return bool(self.redis.exists(key))
        
    async def incr(self, key: str) -> int:
        """Increment value"""
        return self.redis.incr(key)
        
    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration"""
        return bool(self.redis.expire(key, seconds))
        
    async def ttl(self, key: str) -> int:
        """Get key time to live"""
        return self.redis.ttl(key)
        
    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern"""
        return self.redis.keys(pattern)
        
    async def flush(self) -> bool:
        """Flush all keys in current database"""
        return bool(self.redis.flushdb())
        
    async def hash_set(self, name: str, mapping: Dict[str, Any]) -> bool:
        """Set hash mapping"""
        try:
            serialized_mapping = {
                k: json.dumps(v)
                for k, v in mapping.items()
            }
            return bool(self.redis.hset(name, mapping=serialized_mapping))
        except (TypeError, json.JSONEncodeError):
            return False
            
    async def hash_get(self, name: str, key: str) -> Optional[Any]:
        """Get hash value"""
        try:
            value = self.redis.hget(name, key)
            if value is None:
                return None
            return json.loads(value)
        except (json.JSONDecodeError, pickle.UnpicklingError):
            return None
            
    async def hash_getall(self, name: str) -> Dict[str, Any]:
        """Get all hash values"""
        try:
            mapping = self.redis.hgetall(name)
            return {
                k: json.loads(v)
                for k, v in mapping.items()
            }
        except (json.JSONDecodeError, pickle.UnpicklingError):
            return {}
            
    async def pipeline(self) -> 'RedisPipeline':
        """Get Redis pipeline"""
        return RedisPipeline(self.redis.pipeline())
        

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
