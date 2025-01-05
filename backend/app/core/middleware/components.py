"""
Middleware Components
PGF Protocol: MIDDLEWARE_002
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import Request, Response
from .base import BaseMiddleware, MiddlewarePriority
import time
from typing import Optional, Dict, Any
import json
from datetime import datetime

class MetricsMiddleware(BaseMiddleware):
    """Collect and track API metrics"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.MEDIUM)
        self.metrics: Dict[str, Any] = {}
    
    async def process_request(self, request: Request) -> Request:
        request.state.start_time = time.time()
        request.state.metrics = {
            "path": request.url.path,
            "method": request.method,
            "client_ip": request.client.host,
            "timestamp": datetime.utcnow().isoformat()
        }
        return request
    
    async def process_response(self, response: Response) -> Response:
        if hasattr(response, "request") and hasattr(response.request.state, "start_time"):
            processing_time = time.time() - response.request.state.start_time
            metrics = {
                **response.request.state.metrics,
                "processing_time": processing_time,
                "status_code": response.status_code
            }
            self.metrics[datetime.utcnow().isoformat()] = metrics
        return response

class CacheMiddleware(BaseMiddleware):
    """Response caching middleware"""
    
    def __init__(self, cache_timeout: int = 300):
        super().__init__(priority=MiddlewarePriority.HIGH)
        self.cache: Dict[str, Any] = {}
        self.cache_timeout = cache_timeout
    
    async def process_request(self, request: Request) -> Request:
        cache_key = f"{request.method}:{request.url.path}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.cache_timeout:
                request.state.cached_response = cached_data["response"]
        return request
    
    async def process_response(self, response: Response) -> Response:
        if response.status_code == 200 and not hasattr(response.request.state, "cached_response"):
            cache_key = f"{response.request.method}:{response.request.url.path}"
            self.cache[cache_key] = {
                "response": response,
                "timestamp": time.time()
            }
        return response

class CompressionMiddleware(BaseMiddleware):
    """Response compression middleware"""
    
    def __init__(self, min_size: int = 1024):
        super().__init__(priority=MiddlewarePriority.MEDIUM)
        self.min_size = min_size
    
    async def process_request(self, request: Request) -> Request:
        return request
    
    async def process_response(self, response: Response) -> Response:
        if len(response.body) > self.min_size:
            response.headers["Content-Encoding"] = "gzip"
            # Add compression logic here
        return response

class CorrelationMiddleware(BaseMiddleware):
    """Request correlation tracking middleware"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.HIGH)
    
    async def process_request(self, request: Request) -> Request:
        correlation_id = request.headers.get("X-Correlation-ID") or str(time.time())
        request.state.correlation_id = correlation_id
        return request
    
    async def process_response(self, response: Response) -> Response:
        if hasattr(response.request.state, "correlation_id"):
            response.headers["X-Correlation-ID"] = response.request.state.correlation_id
        return response

class ErrorHandlingMiddleware(BaseMiddleware):
    """Global error handling middleware"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.CRITICAL)
    
    async def process_request(self, request: Request) -> Request:
        return request
    
    async def process_response(self, response: Response) -> Response:
        if response.status_code >= 400:
            error_response = {
                "status": "error",
                "code": response.status_code,
                "message": response.body.decode(),
                "timestamp": datetime.utcnow().isoformat(),
                "path": response.request.url.path
            }
            response.body = json.dumps(error_response).encode()
            response.headers["Content-Type"] = "application/json"
        return response
