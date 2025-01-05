# Performance Tuning Guide

## Overview
This guide provides comprehensive information about optimizing the performance of the Kundli Calculation Service, including database optimization, caching strategies, and resource management.

## Table of Contents
1. [Performance Metrics](#performance-metrics)
2. [Database Optimization](#database-optimization)
3. [Caching Strategies](#caching-strategies)
4. [Resource Management](#resource-management)
5. [API Optimization](#api-optimization)
6. [Monitoring and Profiling](#monitoring-and-profiling)

## Performance Metrics

### 1. Key Performance Indicators (KPIs)
```yaml
metrics:
  response_time:
    p95: < 500ms
    p99: < 1000ms
  
  throughput:
    requests_per_second: > 100
    concurrent_users: > 1000
  
  error_rate:
    5xx_errors: < 0.1%
    4xx_errors: < 1%
  
  resource_utilization:
    cpu: < 80%
    memory: < 80%
    disk_io: < 70%
```

### 2. Monitoring Setup
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

REQUEST_COUNT = Counter(
    'request_count_total',
    'Total request count',
    ['endpoint', 'status']
)

# Resource metrics
RESOURCE_USAGE = Gauge(
    'resource_usage_percent',
    'Resource usage percentage',
    ['resource_type']
)
```

## Database Optimization

### 1. Index Optimization
```python
# MongoDB indexes
async def create_indexes():
    await db.kundlis.create_indexes([
        IndexModel([("user_id", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([
            ("date", ASCENDING),
            ("time", ASCENDING)
        ]),
        IndexModel([
            ("latitude", ASCENDING),
            ("longitude", ASCENDING)
        ])
    ])

# Index usage analysis
async def analyze_index_usage():
    return await db.command("aggregate", "system.profile", {
        "pipeline": [
            {"$group": {
                "_id": "$queryPlanner.winningPlan.inputStage.indexName",
                "count": {"$sum": 1}
            }}
        ]
    })
```

### 2. Query Optimization
```python
# Optimized query patterns
class QueryOptimizer:
    async def find_kundli(self, criteria):
        # Use projection to limit fields
        projection = {
            "planets": 1,
            "houses": 1,
            "_id": 0
        }
        
        # Use index hints
        return await db.kundlis.find_one(
            criteria,
            projection=projection,
            hint=[("date", 1), ("time", 1)]
        )
    
    async def batch_find(self, criteria_list):
        # Use bulk operations
        operations = [
            {"$match": criteria} 
            for criteria in criteria_list
        ]
        
        return await db.kundlis.aggregate(operations)
```

### 3. Connection Pooling
```python
# MongoDB connection pool
MONGODB_SETTINGS = {
    "max_pool_size": 100,
    "min_pool_size": 10,
    "max_idle_time_ms": 10000,
    "wait_queue_timeout_ms": 5000
}

client = AsyncIOMotorClient(
    MONGODB_URI,
    **MONGODB_SETTINGS
)
```

## Caching Strategies

### 1. Multi-Level Caching
```python
from typing import Optional, Any
from abc import ABC, abstractmethod

class CacheLayer(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int) -> None:
        pass

class MemoryCache(CacheLayer):
    def __init__(self):
        self.cache = {}
    
    async def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: int) -> None:
        self.cache[key] = value

class RedisCache(CacheLayer):
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: Any, ttl: int) -> None:
        await self.redis.setex(key, ttl, value)

class CacheManager:
    def __init__(self):
        self.memory_cache = MemoryCache()
        self.redis_cache = RedisCache(redis_client)
    
    async def get(self, key: str) -> Optional[Any]:
        # Try memory cache first
        value = await self.memory_cache.get(key)
        if value:
            return value
        
        # Try Redis cache
        value = await self.redis_cache.get(key)
        if value:
            # Update memory cache
            await self.memory_cache.set(key, value, ttl=300)
            return value
        
        return None
```

### 2. Cache Invalidation
```python
class CacheInvalidator:
    def __init__(self, cache_manager):
        self.cache = cache_manager
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern"""
        keys = await self.cache.redis.keys(pattern)
        if keys:
            await self.cache.redis.delete(*keys)
    
    async def invalidate_user_data(self, user_id: str):
        """Invalidate all user-related caches"""
        patterns = [
            f"user:{user_id}:*",
            f"kundli:{user_id}:*"
        ]
        for pattern in patterns:
            await self.invalidate_pattern(pattern)
```

## Resource Management

### 1. Connection Pooling
```python
class ConnectionPool:
    def __init__(self, max_size: int = 100):
        self.pool = asyncio.Queue(max_size)
        self.size = 0
        self.max_size = max_size
    
    async def acquire(self):
        if self.size < self.max_size and self.pool.empty():
            self.size += 1
            return await self.create_connection()
        
        return await self.pool.get()
    
    async def release(self, conn):
        await self.pool.put(conn)
    
    async def create_connection(self):
        # Implementation specific to connection type
        pass
```

### 2. Thread Pool Management
```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

class ThreadPoolManager:
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def run_in_thread(self, func, *args):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            func,
            *args
        )
```

## API Optimization

### 1. Request Batching
```python
class BatchProcessor:
    def __init__(self, max_batch_size: int = 100):
        self.max_batch_size = max_batch_size
    
    async def process_batch(self, items: list):
        if len(items) > self.max_batch_size:
            raise ValueError("Batch size too large")
        
        tasks = [
            self.process_item(item)
            for item in items
        ]
        
        return await asyncio.gather(*tasks)
```

### 2. Response Compression
```python
from fastapi import Response
import gzip

def compress_response(content: bytes) -> Response:
    compressed = gzip.compress(content)
    return Response(
        content=compressed,
        headers={
            "Content-Encoding": "gzip",
            "Vary": "Accept-Encoding"
        }
    )
```

## Monitoring and Profiling

### 1. Performance Profiling
```python
import cProfile
import pstats
import io

class Profiler:
    def __init__(self):
        self.pr = cProfile.Profile()
    
    def start(self):
        self.pr.enable()
    
    def stop(self):
        self.pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        return s.getvalue()
```

### 2. Resource Monitoring
```python
import psutil

class ResourceMonitor:
    @staticmethod
    def get_metrics():
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict()
        }
    
    @staticmethod
    async def monitor_resources(interval: int = 60):
        while True:
            metrics = ResourceMonitor.get_metrics()
            await store_metrics(metrics)
            await asyncio.sleep(interval)
```

### 3. Performance Alerts
```python
class PerformanceAlerts:
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds
    
    async def check_metrics(self, metrics: dict):
        alerts = []
        
        for metric, value in metrics.items():
            threshold = self.thresholds.get(metric)
            if threshold and value > threshold:
                alerts.append({
                    "metric": metric,
                    "value": value,
                    "threshold": threshold,
                    "timestamp": datetime.utcnow()
                })
        
        if alerts:
            await self.send_alerts(alerts)
    
    async def send_alerts(self, alerts: list):
        # Implementation for sending alerts
        pass
```
