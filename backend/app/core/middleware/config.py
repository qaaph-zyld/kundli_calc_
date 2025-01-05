"""
Middleware Configuration
PGF Protocol: MIDDLEWARE_003
Gate: GATE_4
Version: 1.0.0
"""

from typing import List
from fastapi import FastAPI
from .base import MiddlewareChain
from .components import (
    MetricsMiddleware,
    CacheMiddleware,
    CompressionMiddleware,
    CorrelationMiddleware,
    ErrorHandlingMiddleware
)
from ..security.middleware import AuthenticationMiddleware, SecurityMiddleware
from ..performance.middleware import PerformanceMiddleware

class MiddlewareConfig:
    """Configure and manage application middleware"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.middleware_chain = MiddlewareChain()
    
    def configure_middleware(self) -> None:
        """Configure all middleware components"""
        # Add middleware in priority order (security first, then performance)
        self.middleware_chain.add_middleware(SecurityMiddleware())
        self.middleware_chain.add_middleware(AuthenticationMiddleware())
        self.middleware_chain.add_middleware(PerformanceMiddleware())
        self.middleware_chain.add_middleware(ErrorHandlingMiddleware())
        self.middleware_chain.add_middleware(CorrelationMiddleware())
        self.middleware_chain.add_middleware(CacheMiddleware())
        self.middleware_chain.add_middleware(MetricsMiddleware())
        self.middleware_chain.add_middleware(CompressionMiddleware())
        
        # Build and add middleware chain to app
        self.app.middleware("http")(self.middleware_chain.build_chain())
    
    @property
    def metrics(self) -> dict:
        """Get collected metrics"""
        for middleware in self.middleware_chain._middlewares.values():
            if isinstance(middleware, MetricsMiddleware):
                return middleware.metrics
        return {}
    
    @property
    def cache_stats(self) -> dict:
        """Get cache statistics"""
        for middleware in self.middleware_chain._middlewares.values():
            if isinstance(middleware, CacheMiddleware):
                return {
                    "size": len(middleware.cache),
                    "items": middleware.cache
                }
        return {}
