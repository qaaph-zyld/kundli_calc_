"""
API Gateway Framework
PGF Protocol: GWY_001
Gate: GATE_13
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Callable
from enum import Enum
from datetime import datetime, timedelta
import asyncio
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import httpx
import redis.asyncio as redis
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)

class RouteType(str, Enum):
    """Route types"""
    PUBLIC = "public"
    PROTECTED = "protected"
    ADMIN = "admin"

class LoadBalanceStrategy(str, Enum):
    """Load balance strategies"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    IP_HASH = "ip_hash"

class CacheStrategy(str, Enum):
    """Cache strategies"""
    NO_CACHE = "no_cache"
    SIMPLE = "simple"
    SMART = "smart"

class RateLimitType(str, Enum):
    """Rate limit types"""
    IP = "ip"
    USER = "user"
    API_KEY = "api_key"
    GLOBAL = "global"

class ServiceHealth(str, Enum):
    """Service health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class RouteConfig(BaseModel):
    """Route configuration"""
    
    path: str
    type: RouteType
    methods: List[str]
    upstream_service: str
    timeout: int = 30
    retry_count: int = 3
    circuit_breaker_threshold: int = 5
    rate_limit: Optional[int] = None
    rate_limit_type: Optional[RateLimitType] = None
    cache_strategy: CacheStrategy = CacheStrategy.NO_CACHE
    cache_ttl: Optional[int] = None
    cors_enabled: bool = False
    compression_enabled: bool = True
    auth_required: bool = True
    roles_required: Optional[List[str]] = None

class ServiceConfig(BaseModel):
    """Service configuration"""
    
    name: str
    hosts: List[str]
    health_check_path: str = "/health"
    health_check_interval: int = 30
    weight: int = 1
    max_connections: int = 100
    ssl_verify: bool = True

class GatewayConfig(BaseModel):
    """Gateway configuration"""
    
    routes: Dict[str, RouteConfig]
    services: Dict[str, ServiceConfig]
    load_balance_strategy: LoadBalanceStrategy = LoadBalanceStrategy.ROUND_ROBIN
    default_timeout: int = 30
    max_retries: int = 3
    enable_circuit_breaker: bool = True
    enable_rate_limiting: bool = True
    enable_caching: bool = True
    trusted_hosts: List[str] = Field(default_factory=list)
    cors_origins: List[str] = Field(default_factory=list)
    jwt_secret: str
    jwt_algorithm: str = "HS256"

class ServiceRegistry:
    """Service registry"""
    
    def __init__(self, config: GatewayConfig):
        self.config = config
        self.services: Dict[str, List[ServiceHealth]] = {}
        self.connections: Dict[str, int] = {}
        self._setup_services()
    
    def _setup_services(self) -> None:
        """Setup services"""
        for name, service in self.config.services.items():
            self.services[name] = [ServiceHealth.HEALTHY] * len(service.hosts)
            self.connections[name] = 0
    
    def get_service_url(
        self,
        service_name: str,
        request: Optional[Request] = None
    ) -> str:
        """Get service URL based on load balance strategy"""
        service = self.config.services[service_name]
        healthy_indices = [
            i for i, health in enumerate(self.services[service_name])
            if health == ServiceHealth.HEALTHY
        ]
        
        if not healthy_indices:
            raise AppError(
                code=ErrorCode.SERVICE_UNAVAILABLE,
                message=f"Service {service_name} is unavailable",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH
            )
        
        strategy = self.config.load_balance_strategy
        if strategy == LoadBalanceStrategy.ROUND_ROBIN:
            index = healthy_indices[self.connections[service_name] % len(healthy_indices)]
            self.connections[service_name] += 1
        
        elif strategy == LoadBalanceStrategy.LEAST_CONNECTIONS:
            index = min(
                healthy_indices,
                key=lambda i: self.connections.get(f"{service_name}_{i}", 0)
            )
        
        elif strategy == LoadBalanceStrategy.WEIGHTED:
            weights = [service.weight if i in healthy_indices else 0
                      for i in range(len(service.hosts))]
            import random
            index = random.choices(
                range(len(service.hosts)),
                weights=weights
            )[0]
        
        elif strategy == LoadBalanceStrategy.IP_HASH:
            if not request:
                index = healthy_indices[0]
            else:
                import hashlib
                hash_value = int(hashlib.md5(
                    request.client.host.encode()
                ).hexdigest(), 16)
                index = healthy_indices[hash_value % len(healthy_indices)]
        
        return service.hosts[index]

    async def check_service_health(self, name: str, index: int) -> None:
        """Check service health"""
        service = self.config.services[name]
        url = f"{service.hosts[index]}{service.health_check_path}"
        
        try:
            async with httpx.AsyncClient(
                verify=service.ssl_verify,
                timeout=5
            ) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    self.services[name][index] = ServiceHealth.HEALTHY
                else:
                    self.services[name][index] = ServiceHealth.DEGRADED
        
        except Exception:
            self.services[name][index] = ServiceHealth.UNHEALTHY

class CircuitBreaker:
    """Circuit breaker"""
    
    def __init__(self, threshold: int = 5, reset_timeout: int = 60):
        self.threshold = threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function with circuit breaker"""
        if self.state == "open":
            if (datetime.utcnow() - self.last_failure_time
                    > timedelta(seconds=self.reset_timeout)):
                self.state = "half-open"
            else:
                raise AppError(
                    code=ErrorCode.SERVICE_UNAVAILABLE,
                    message="Circuit breaker is open",
                    category=ErrorCategory.SYSTEM,
                    severity=ErrorSeverity.HIGH
                )
        
        try:
            result = await func(*args, **kwargs)
            
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.utcnow()
            
            if self.failures >= self.threshold:
                self.state = "open"
            
            raise e

class RateLimiter:
    """Rate limiter"""
    
    def __init__(
        self,
        redis_client: redis.Redis,
        window_size: int = 60,
        max_requests: int = 100
    ):
        self.redis = redis_client
        self.window_size = window_size
        self.max_requests = max_requests
    
    async def check_rate_limit(
        self,
        key: str,
        limit_type: RateLimitType
    ) -> bool:
        """Check if rate limit is exceeded"""
        redis_key = f"rate_limit:{limit_type}:{key}"
        
        pipe = self.redis.pipeline()
        now = datetime.utcnow().timestamp()
        window_start = now - self.window_size
        
        # Remove old requests
        await pipe.zremrangebyscore(redis_key, 0, window_start)
        
        # Add current request
        await pipe.zadd(redis_key, {str(now): now})
        
        # Get request count
        await pipe.zcard(redis_key)
        
        # Set expiry
        await pipe.expire(redis_key, self.window_size)
        
        results = await pipe.execute()
        request_count = results[2]
        
        return request_count <= self.max_requests

class APIGateway:
    """API Gateway"""
    
    def __init__(
        self,
        app: FastAPI,
        config: GatewayConfig,
        redis_client: redis.Redis
    ):
        self.app = app
        self.config = config
        self.registry = ServiceRegistry(config)
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.rate_limiter = RateLimiter(redis_client)
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self) -> None:
        """Setup middleware"""
        # CORS middleware
        if self.config.cors_origins:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.config.cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
        
        # Trusted host middleware
        if self.config.trusted_hosts:
            self.app.add_middleware(
                TrustedHostMiddleware,
                allowed_hosts=self.config.trusted_hosts
            )
        
        # Compression middleware
        self.app.add_middleware(GZipMiddleware)
        
        # Gateway middleware
        self.app.add_middleware(
            BaseHTTPMiddleware,
            dispatch=self._gateway_middleware
        )
    
    def _setup_routes(self) -> None:
        """Setup routes"""
        for path, route in self.config.routes.items():
            self.circuit_breakers[path] = CircuitBreaker(
                threshold=route.circuit_breaker_threshold
            )
    
    async def _verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret,
                algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except jwt.InvalidTokenError:
            raise AppError(
                code=ErrorCode.INVALID_TOKEN,
                message="Invalid authentication token",
                category=ErrorCategory.AUTHENTICATION,
                severity=ErrorSeverity.MEDIUM
            )
    
    async def _check_auth(
        self,
        request: Request,
        route: RouteConfig
    ) -> None:
        """Check authentication and authorization"""
        if not route.auth_required:
            return
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AppError(
                code=ErrorCode.UNAUTHORIZED,
                message="Missing authentication token",
                category=ErrorCategory.AUTHENTICATION,
                severity=ErrorSeverity.MEDIUM
            )
        
        token = auth_header.split(" ")[1]
        payload = await self._verify_token(token)
        
        if route.roles_required:
            user_roles = payload.get("roles", [])
            if not any(role in user_roles for role in route.roles_required):
                raise AppError(
                    code=ErrorCode.INSUFFICIENT_PERMISSIONS,
                    message="Insufficient permissions",
                    category=ErrorCategory.AUTHORIZATION,
                    severity=ErrorSeverity.HIGH
                )
    
    async def _check_rate_limit(
        self,
        request: Request,
        route: RouteConfig
    ) -> None:
        """Check rate limit"""
        if not route.rate_limit or not route.rate_limit_type:
            return
        
        if route.rate_limit_type == RateLimitType.IP:
            key = request.client.host
        elif route.rate_limit_type == RateLimitType.USER:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = await self._verify_token(token)
                key = payload.get("sub", "anonymous")
            else:
                key = "anonymous"
        elif route.rate_limit_type == RateLimitType.API_KEY:
            key = request.headers.get("X-API-Key", "anonymous")
        else:  # GLOBAL
            key = "*"
        
        if not await self.rate_limiter.check_rate_limit(
            key,
            route.rate_limit_type
        ):
            raise AppError(
                code=ErrorCode.TOO_MANY_REQUESTS,
                message="Rate limit exceeded",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM
            )
    
    async def _gateway_middleware(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Gateway middleware"""
        path = request.url.path
        route_config = self.config.routes.get(path)
        
        if not route_config:
            return await call_next(request)
        
        try:
            # Check authentication and authorization
            await self._check_auth(request, route_config)
            
            # Check rate limit
            await self._check_rate_limit(request, route_config)
            
            # Get upstream service URL
            service_url = self.registry.get_service_url(
                route_config.upstream_service,
                request
            )
            
            # Forward request
            async def forward_request():
                url = f"{service_url}{path}"
                timeout = httpx.Timeout(route_config.timeout)
                
                async with httpx.AsyncClient(
                    timeout=timeout,
                    follow_redirects=True
                ) as client:
                    response = await client.request(
                        method=request.method,
                        url=url,
                        headers=request.headers,
                        params=request.query_params,
                        content=await request.body()
                    )
                    return Response(
                        content=response.content,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
            
            # Apply circuit breaker
            circuit_breaker = self.circuit_breakers[path]
            response = await circuit_breaker.call(forward_request)
            
            return response
            
        except Exception as e:
            if isinstance(e, AppError):
                raise e
            raise AppError(
                code=ErrorCode.GATEWAY_ERROR,
                message="Gateway error occurred",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
