"""
Base Middleware Framework
PGF Protocol: MIDDLEWARE_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Callable, Dict, Any, Optional
from fastapi import Request, Response
from abc import ABC, abstractmethod
import time
import asyncio
from datetime import datetime
from enum import Enum

class MiddlewarePriority(int, Enum):
    """Middleware execution priority levels"""
    CRITICAL = 0    # Authentication, Security
    HIGH = 1        # Caching, Rate Limiting
    MEDIUM = 2      # Logging, Metrics
    LOW = 3         # Analytics, Debug

class BaseMiddleware(ABC):
    """Base middleware class with priority-based execution"""
    
    def __init__(self, priority: MiddlewarePriority = MiddlewarePriority.MEDIUM):
        self.priority = priority
        self.next_middleware: Optional[BaseMiddleware] = None
    
    @abstractmethod
    async def process_request(self, request: Request) -> Request:
        """Process incoming request"""
        pass
    
    @abstractmethod
    async def process_response(self, response: Response) -> Response:
        """Process outgoing response"""
        pass
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Execute middleware chain"""
        try:
            # Pre-processing
            modified_request = await self.process_request(request)
            
            # Call next middleware or endpoint
            response = await call_next(modified_request)
            
            # Post-processing
            modified_response = await self.process_response(response)
            
            return modified_response
            
        except Exception as e:
            # Log error and reraise
            print(f"Error in middleware {self.__class__.__name__}: {str(e)}")
            raise

class MiddlewareChain:
    """Manages middleware execution chain"""
    
    def __init__(self):
        self._middlewares: Dict[MiddlewarePriority, list[BaseMiddleware]] = {
            priority: [] for priority in MiddlewarePriority
        }
    
    def add_middleware(self, middleware: BaseMiddleware) -> None:
        """Add middleware to chain"""
        self._middlewares[middleware.priority].append(middleware)
    
    def build_chain(self) -> Callable:
        """Build middleware execution chain"""
        # Sort middlewares by priority
        sorted_middlewares = []
        for priority in sorted(MiddlewarePriority):
            sorted_middlewares.extend(self._middlewares[priority])
        
        # Link middlewares
        for i in range(len(sorted_middlewares) - 1):
            sorted_middlewares[i].next_middleware = sorted_middlewares[i + 1]
        
        async def middleware_chain(request: Request, call_next: Callable) -> Response:
            """Execute complete middleware chain"""
            if not sorted_middlewares:
                return await call_next(request)
                
            return await sorted_middlewares[0](request, call_next)
        
        return middleware_chain
