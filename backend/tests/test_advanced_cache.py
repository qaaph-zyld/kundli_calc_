"""
Test Suite for Advanced Caching System
PGF Protocol: CACHE_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from app.core.caching.advanced_cache import (
    AdvancedCache,
    CacheMetrics,
    cached
)

@pytest.fixture
def cache():
    return AdvancedCache[str](
        max_size=10,
        max_memory_mb=1.0,
        default_ttl=3600,
        eviction_policy="adaptive"
    )

@pytest.mark.asyncio
async def test_basic_operations(cache):
    """Test basic cache operations"""
    # Put and get
    await cache.put("key1", "value1")
    result = await cache.get("key1")
    assert result == "value1"
    
    # Missing key
    result = await cache.get("missing_key")
    assert result is None
    
    # Overwrite
    await cache.put("key1", "value2")
    result = await cache.get("key1")
    assert result == "value2"

@pytest.mark.asyncio
async def test_ttl_expiration(cache):
    """Test TTL-based expiration"""
    # Put with short TTL
    await cache.put("key1", "value1", ttl=1)
    
    # Verify immediate access
    result = await cache.get("key1")
    assert result == "value1"
    
    # Wait for expiration
    await asyncio.sleep(1.1)
    
    # Verify expiration
    result = await cache.get("key1")
    assert result is None

@pytest.mark.asyncio
async def test_max_size_eviction(cache):
    """Test size-based eviction"""
    # Fill cache
    for i in range(15):
        await cache.put(f"key{i}", f"value{i}")
    
    # Verify size limit
    metrics = await cache.get_metrics()
    assert metrics["cache_size"] <= 10
    
    # Verify eviction
    assert metrics["evictions"] > 0

@pytest.mark.asyncio
async def test_eviction_policies(cache):
    """Test different eviction policies"""
    # Test LRU
    cache.eviction_policy = "lru"
    for i in range(5):
        await cache.put(f"key{i}", f"value{i}")
    
    # Access some items
    await cache.get("key1")
    await cache.get("key3")
    
    # Force eviction
    for i in range(5, 15):
        await cache.put(f"key{i}", f"value{i}")
    
    # Recently used items should still be present
    assert await cache.get("key1") is not None
    assert await cache.get("key3") is not None
    
    # Test Cost-based
    cache.eviction_policy = "cost"
    await cache.put("expensive", "value", cost=10.0)
    await cache.put("cheap", "value", cost=0.1)
    
    # Force eviction
    for i in range(20):
        await cache.put(f"key{i}", f"value{i}")
    
    # Cheap item should survive longer
    assert await cache.get("cheap") is not None
    assert await cache.get("expensive") is None

@pytest.mark.asyncio
async def test_metrics(cache):
    """Test metrics tracking"""
    # Generate some activity
    await cache.put("key1", "value1")
    await cache.get("key1")  # Hit
    await cache.get("missing")  # Miss
    
    metrics = await cache.get_metrics()
    
    assert metrics["hits"] == 1
    assert metrics["misses"] == 1
    assert metrics["hit_ratio"] == 0.5
    assert metrics["cache_size"] == 1
    assert metrics["memory_usage_mb"] >= 0
    assert metrics["avg_access_time"] >= 0

@pytest.mark.asyncio
async def test_concurrent_access(cache):
    """Test concurrent cache access"""
    async def worker(id: int):
        for i in range(100):
            key = f"key{id}_{i}"
            await cache.put(key, f"value{id}_{i}")
            await cache.get(key)
    
    # Run multiple workers
    workers = [worker(i) for i in range(5)]
    await asyncio.gather(*workers)
    
    metrics = await cache.get_metrics()
    assert metrics["hits"] > 0
    assert metrics["cache_size"] <= cache.max_size

@pytest.mark.asyncio
async def test_decorator():
    """Test cache decorator"""
    cache = AdvancedCache[int](max_size=100)
    call_count = 0
    
    @cached(cache)
    async def expensive_calculation(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call should calculate
    result1 = await expensive_calculation(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call should use cache
    result2 = await expensive_calculation(5)
    assert result2 == 10
    assert call_count == 1  # Unchanged
    
    # Different input should calculate
    result3 = await expensive_calculation(6)
    assert result3 == 12
    assert call_count == 2

@pytest.mark.asyncio
async def test_cleanup(cache):
    """Test cleanup of expired items"""
    # Add items with short TTL
    for i in range(5):
        await cache.put(f"key{i}", f"value{i}", ttl=1)
    
    # Wait for expiration
    await asyncio.sleep(1.1)
    
    # Run cleanup
    cleaned = await cache.cleanup_expired()
    assert cleaned == 5
    
    # Verify all expired items are removed
    for i in range(5):
        assert await cache.get(f"key{i}") is None

@pytest.mark.asyncio
async def test_clear(cache):
    """Test cache clearing"""
    # Add some items
    for i in range(5):
        await cache.put(f"key{i}", f"value{i}")
    
    # Clear cache
    await cache.clear()
    
    metrics = await cache.get_metrics()
    assert metrics["cache_size"] == 0
    assert metrics["hits"] == 0
    assert metrics["misses"] == 0

@pytest.mark.asyncio
async def test_memory_limit(cache):
    """Test memory limit enforcement"""
    # Add large items
    large_data = "x" * 1000000  # 1MB string
    await cache.put("large1", large_data)
    
    metrics = await cache.get_metrics()
    assert metrics["memory_usage_mb"] <= cache.max_memory_mb
    
    # Try to add another large item
    await cache.put("large2", large_data)
    
    # Verify memory limit
    metrics = await cache.get_metrics()
    assert metrics["memory_usage_mb"] <= cache.max_memory_mb
