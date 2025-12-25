"""Cache module initialization"""
from typing import Optional, Any, Dict
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Import calculation cache
from .calculation_cache import CalculationCache

class RedisCache:
    """Redis cache implementation with fallback for tests"""
    _instance: Optional['RedisCache'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._fallback_mode = os.environ.get("ENV") == "test"
            self._memory_cache: Dict[str, Any] = {}
            self.redis = None
            
            if self._fallback_mode:
                logger.info("Cache running in test/fallback mode")
                self.initialized = True
                return
                
            try:
                import redis as redis_lib
                redis_url = os.environ.get("REDIS_URL")
                if redis_url:
                    parsed = urlparse(redis_url)
                    redis_host = parsed.hostname or "localhost"
                    redis_port = parsed.port or 6379
                    redis_db = int((parsed.path or "/0").lstrip("/") or 0)
                else:
                    redis_host = os.environ.get("REDIS_HOST", "localhost")
                    redis_port = int(os.environ.get("REDIS_PORT", "6379"))
                    redis_db = int(os.environ.get("REDIS_DB", "0"))
                self.redis = redis_lib.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True
                )
                self.redis.ping()  # Test connection
                self.initialized = True
            except Exception as e:
                logger.warning(f"Redis connection failed, using fallback: {e}")
                self._fallback_mode = True
                self.redis = None
                self.initialized = True
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if self._fallback_mode:
            return self._memory_cache.get(key)
        if self.redis:
            try:
                return self.redis.get(key)
            except Exception:
                return self._memory_cache.get(key)
        return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        if self._fallback_mode:
            self._memory_cache[key] = value
            return True
        if self.redis:
            try:
                return bool(self.redis.set(key, str(value) if not isinstance(value, str) else value, ex=expire))
            except Exception:
                self._memory_cache[key] = value
                return True
        return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if self._fallback_mode:
            return self._memory_cache.pop(key, None) is not None
        if self.redis:
            try:
                return bool(self.redis.delete(key))
            except Exception:
                return self._memory_cache.pop(key, None) is not None
        return False

# Global cache instances
calculation_cache = CalculationCache()
redis_cache = RedisCache()
cache = redis_cache  # Alias for compatibility with monitoring module
