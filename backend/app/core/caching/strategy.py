"""
Caching Strategy Framework
PGF Protocol: CACHE_002
Gate: GATE_6
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from .engine import CacheEngine, cached

class DataType(str, Enum):
    """Data types for caching"""
    KUNDLI = "kundli"
    PATTERN = "pattern"
    USER = "user"
    SYSTEM = "system"

class CachePolicy(BaseModel):
    """Cache policy"""
    
    data_type: DataType
    ttl: int
    key_prefix: str
    invalidation_events: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CacheManager:
    """Cache manager for policy-based caching"""
    
    def __init__(self, cache_engine: CacheEngine):
        self.cache = cache_engine
        self.policies: Dict[DataType, CachePolicy] = {}
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default cache policies"""
        # Kundli data policy
        self.add_policy(CachePolicy(
            data_type=DataType.KUNDLI,
            ttl=300,  # 5 minutes
            key_prefix="kundli",
            invalidation_events=[
                "kundli_update",
                "kundli_delete"
            ]
        ))
        
        # Pattern data policy
        self.add_policy(CachePolicy(
            data_type=DataType.PATTERN,
            ttl=600,  # 10 minutes
            key_prefix="pattern",
            invalidation_events=[
                "pattern_update",
                "pattern_delete"
            ],
            dependencies=["kundli"]
        ))
        
        # User data policy
        self.add_policy(CachePolicy(
            data_type=DataType.USER,
            ttl=1800,  # 30 minutes
            key_prefix="user",
            invalidation_events=[
                "user_update",
                "user_delete"
            ]
        ))
        
        # System data policy
        self.add_policy(CachePolicy(
            data_type=DataType.SYSTEM,
            ttl=3600,  # 1 hour
            key_prefix="system",
            invalidation_events=[
                "system_update",
                "config_update"
            ]
        ))
    
    def add_policy(self, policy: CachePolicy) -> None:
        """Add new cache policy"""
        self.policies[policy.data_type] = policy
    
    def get_policy(self, data_type: DataType) -> Optional[CachePolicy]:
        """Get cache policy by data type"""
        return self.policies.get(data_type)
    
    def build_key(self, data_type: DataType, *parts: str) -> str:
        """Build cache key using policy prefix"""
        policy = self.get_policy(data_type)
        if not policy:
            raise ValueError(f"No cache policy found for {data_type}")
            
        key_parts = [policy.key_prefix]
        key_parts.extend(parts)
        return ":".join(key_parts)
    
    async def invalidate(
        self,
        data_type: DataType,
        event: str,
        key: Optional[str] = None
    ) -> None:
        """Invalidate cache based on event"""
        policy = self.get_policy(data_type)
        if not policy:
            return
            
        if event in policy.invalidation_events:
            if key:
                # Invalidate specific key
                await self.cache.delete(self.build_key(data_type, key))
            else:
                # Invalidate all keys with prefix
                if self.cache.config.backend == "redis":
                    pattern = f"{policy.key_prefix}:*"
                    keys = await self.cache._redis.keys(pattern)
                    if keys:
                        await self.cache._redis.delete(*keys)
                else:
                    # For memory cache, clear all entries with prefix
                    keys_to_delete = [
                        k for k in self.cache._cache.keys()
                        if k.startswith(f"{policy.key_prefix}:")
                    ]
                    for k in keys_to_delete:
                        await self.cache.delete(k)
            
            # Invalidate dependent caches
            for dep in policy.dependencies:
                await self.invalidate(dep, f"{data_type}_{event}")
    
    def cached_kundli(self, ttl: Optional[int] = None):
        """Decorator for caching Kundli data"""
        policy = self.get_policy(DataType.KUNDLI)
        return cached(
            ttl=ttl or policy.ttl,
            key_builder=lambda *args, **kwargs: self.build_key(
                DataType.KUNDLI,
                str(kwargs.get("kundli_id") or args[0])
            )
        )
    
    def cached_pattern(self, ttl: Optional[int] = None):
        """Decorator for caching pattern data"""
        policy = self.get_policy(DataType.PATTERN)
        return cached(
            ttl=ttl or policy.ttl,
            key_builder=lambda *args, **kwargs: self.build_key(
                DataType.PATTERN,
                str(kwargs.get("kundli_id") or args[0])
            )
        )
    
    def cached_user(self, ttl: Optional[int] = None):
        """Decorator for caching user data"""
        policy = self.get_policy(DataType.USER)
        return cached(
            ttl=ttl or policy.ttl,
            key_builder=lambda *args, **kwargs: self.build_key(
                DataType.USER,
                str(kwargs.get("user_id") or args[0])
            )
        )
    
    def cached_system(self, ttl: Optional[int] = None):
        """Decorator for caching system data"""
        policy = self.get_policy(DataType.SYSTEM)
        return cached(
            ttl=ttl or policy.ttl,
            key_builder=lambda *args, **kwargs: self.build_key(
                DataType.SYSTEM,
                str(kwargs.get("key") or args[0])
            )
        )

# Global cache manager instance
cache_manager = CacheManager(cache_engine)
