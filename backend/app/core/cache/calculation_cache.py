"""Cache implementation for astronomical calculations."""

import hashlib
import json
import time
from datetime import datetime
from functools import wraps
from threading import RLock
from typing import Any, Dict, Optional


class CalculationCache:
    """Thread-safe cache for astronomical calculations with TTL support."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """Initialize cache with size limit.

        Args:
            max_size: Maximum number of items to store in cache
            default_ttl: Default time-to-live in seconds (default 1 hour)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = RLock()
        self._hits = 0
        self._misses = 0

    def generate_key(self, *args: Any) -> str:
        """Generate a unique cache key from arguments.

        Args:
            *args: Variable arguments to use for key generation

        Returns:
            Unique hash string for the arguments
        """
        # Convert datetime objects to ISO format strings
        processed_args = []
        for arg in args:
            if isinstance(arg, datetime):
                processed_args.append(arg.isoformat())
            else:
                processed_args.append(str(arg))

        # Create a string representation and hash it
        key_str = json.dumps(processed_args, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value if found, None otherwise
        """
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Check if entry is expired
                if time.time() - entry["timestamp"] > entry.get("ttl", self._default_ttl):
                    del self._cache[key]
                    self._misses += 1
                    return None
                self._hits += 1
                return entry["value"]
            self._misses += 1
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key to set
            value: Value to cache
            ttl: Time-to-live in seconds (optional)
        """
        with self._lock:
            # Evict oldest entry if cache is full
            if len(self._cache) >= self._max_size and key not in self._cache:
                # Remove first item (oldest)
                self._cache.pop(next(iter(self._cache)))

            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
                "ttl": ttl if ttl is not None else self._default_ttl,
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(hit_rate, 2),
            }

    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Get current size of cache.

        Returns:
            Number of items in cache
        """
        with self._lock:
            return len(self._cache)

    def contains(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key to check

        Returns:
            True if key exists, False otherwise
        """
        with self._lock:
            return key in self._cache
