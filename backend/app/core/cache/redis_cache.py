"""Redis Caching Layer
====================
High-performance caching for calculation results and API responses.

Features:
- Automatic cache invalidation
- Configurable TTL per cache type
- Cache warming for common calculations
- Cache statistics tracking

Author: Kundli Calculation Engine
Date: 2024-12-31
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    import redis
    from redis import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = None

logger = logging.getLogger(__name__)


class CacheConfig:
    """Cache configuration for different data types."""

    CHART_CALCULATION = {"ttl": 3600 * 24 * 7, "prefix": "chart"}  # 7 days

    DASHA_CALCULATION = {"ttl": 3600 * 24 * 30, "prefix": "dasha"}  # 30 days

    DIVISIONAL_CHART = {"ttl": 3600 * 24 * 7, "prefix": "divisional"}  # 7 days

    SHADBALA = {"ttl": 3600 * 24 * 7, "prefix": "shadbala"}  # 7 days

    ASHTAKAVARGA = {"ttl": 3600 * 24 * 7, "prefix": "ashtakavarga"}  # 7 days

    YOGA_DETECTION = {"ttl": 3600 * 24 * 7, "prefix": "yoga"}  # 7 days

    EPHEMERIS = {"ttl": 3600 * 24, "prefix": "ephemeris"}  # 1 day

    PANCHANG = {"ttl": 3600 * 6, "prefix": "panchang"}  # 6 hours


class RedisCache:
    """Redis-based caching layer for Kundli calculations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        enabled: bool = True,
    ):
        self.enabled = enabled and REDIS_AVAILABLE
        self.client: Optional[Redis] = None
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0}

        if self.enabled:
            try:
                self.client = redis.Redis(
                    host=host, port=port, db=db, password=password, decode_responses=True, socket_connect_timeout=5
                )
                self.client.ping()
                logger.info(f"Redis cache connected: {host}:{port}")
            except Exception as e:
                logger.warning(f"Redis not available: {e}. Caching disabled.")
                self.enabled = False
                self.client = None

    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix and hash."""
        hash_key = hashlib.md5(identifier.encode()).hexdigest()
        return f"kundli:{prefix}:{hash_key}"

    def _serialize(self, data: Any) -> str:
        """Serialize data to JSON string."""
        return json.dumps(data, default=str, ensure_ascii=False)

    def _deserialize(self, data: str) -> Any:
        """Deserialize JSON string to data."""
        return json.loads(data)

    def get(self, cache_type: Dict[str, Any], identifier: str) -> Optional[Any]:
        """
        Get cached data.

        Args:
            cache_type: Cache configuration from CacheConfig
            identifier: Unique identifier for the data

        Returns:
            Cached data or None if not found
        """
        if not self.enabled or not self.client:
            return None

        try:
            key = self._generate_key(cache_type["prefix"], identifier)
            data = self.client.get(key)

            if data:
                self.stats["hits"] += 1
                return self._deserialize(data)
            else:
                self.stats["misses"] += 1
                return None

        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, cache_type: Dict[str, Any], identifier: str, data: Any, ttl_override: Optional[int] = None) -> bool:
        """
        Set cached data.

        Args:
            cache_type: Cache configuration from CacheConfig
            identifier: Unique identifier for the data
            data: Data to cache
            ttl_override: Override default TTL in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            key = self._generate_key(cache_type["prefix"], identifier)
            ttl = ttl_override or cache_type["ttl"]
            serialized = self._serialize(data)

            self.client.setex(key, ttl, serialized)
            self.stats["sets"] += 1
            return True

        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, cache_type: Dict[str, Any], identifier: str) -> bool:
        """
        Delete cached data.

        Args:
            cache_type: Cache configuration from CacheConfig
            identifier: Unique identifier for the data

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.client:
            return False

        try:
            key = self._generate_key(cache_type["prefix"], identifier)
            self.client.delete(key)
            self.stats["deletes"] += 1
            return True

        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern.

        Args:
            pattern: Redis key pattern (e.g., "kundli:chart:*")

        Returns:
            Number of keys deleted
        """
        if not self.enabled or not self.client:
            return 0

        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0

        except Exception as e:
            logger.error(f"Cache delete pattern error: {e}")
            return 0

    def clear_all(self) -> bool:
        """Clear all cache entries."""
        if not self.enabled or not self.client:
            return False

        try:
            return self.delete_pattern("kundli:*") > 0
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "enabled": self.enabled,
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "deletes": self.stats["deletes"],
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests,
        }

    def health_check(self) -> Dict[str, Any]:
        """Check Redis connection health."""
        if not self.enabled or not self.client:
            return {"status": "disabled", "message": "Redis caching is disabled"}

        try:
            self.client.ping()
            info = self.client.info("memory")

            return {
                "status": "healthy",
                "memory_used": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "stats": self.get_stats(),
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


cache_instance = RedisCache(enabled=False)


def get_cache() -> RedisCache:
    """Get global cache instance."""
    return cache_instance


def init_cache(
    host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None, enabled: bool = True
) -> RedisCache:
    """Initialize global cache instance."""
    global cache_instance
    cache_instance = RedisCache(host, port, db, password, enabled)
    return cache_instance


def cache_chart_calculation(birth_data: Dict[str, Any]) -> str:
    """Generate cache identifier for chart calculation."""
    key_data = {
        "year": birth_data["year"],
        "month": birth_data["month"],
        "day": birth_data["day"],
        "hour": birth_data["hour"],
        "minute": birth_data["minute"],
        "latitude": round(birth_data["latitude"], 4),
        "longitude": round(birth_data["longitude"], 4),
        "ayanamsa": birth_data.get("ayanamsa", "Lahiri"),
    }
    return json.dumps(key_data, sort_keys=True)


def cache_dasha_calculation(birth_data: Dict[str, Any], system: str) -> str:
    """Generate cache identifier for dasha calculation."""
    chart_key = cache_chart_calculation(birth_data)
    return f"{chart_key}:system={system}"


def cache_divisional_chart(birth_data: Dict[str, Any], division: int) -> str:
    """Generate cache identifier for divisional chart."""
    chart_key = cache_chart_calculation(birth_data)
    return f"{chart_key}:D{division}"
