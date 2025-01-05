"""
API Gateway Configuration
PGF Protocol: GWY_002
Gate: GATE_13
Version: 1.0.0
"""

from typing import Dict
from .framework import (
    GatewayConfig,
    RouteConfig,
    ServiceConfig,
    RouteType,
    LoadBalanceStrategy,
    CacheStrategy,
    RateLimitType
)

def get_gateway_config(environment: str) -> GatewayConfig:
    """Get gateway configuration for environment"""
    
    # Route configurations
    routes: Dict[str, RouteConfig] = {
        # Public routes
        "/api/v1/health": RouteConfig(
            path="/api/v1/health",
            type=RouteType.PUBLIC,
            methods=["GET"],
            upstream_service="api",
            auth_required=False,
            cache_strategy=CacheStrategy.NO_CACHE
        ),
        "/api/v1/docs": RouteConfig(
            path="/api/v1/docs",
            type=RouteType.PUBLIC,
            methods=["GET"],
            upstream_service="api",
            auth_required=False,
            cache_strategy=CacheStrategy.SIMPLE,
            cache_ttl=3600
        ),
        
        # Authentication routes
        "/api/v1/auth/login": RouteConfig(
            path="/api/v1/auth/login",
            type=RouteType.PUBLIC,
            methods=["POST"],
            upstream_service="auth",
            auth_required=False,
            rate_limit=100,
            rate_limit_type=RateLimitType.IP
        ),
        "/api/v1/auth/refresh": RouteConfig(
            path="/api/v1/auth/refresh",
            type=RouteType.PUBLIC,
            methods=["POST"],
            upstream_service="auth",
            auth_required=False,
            rate_limit=100,
            rate_limit_type=RateLimitType.IP
        ),
        
        # Protected routes
        "/api/v1/kundli/calculate": RouteConfig(
            path="/api/v1/kundli/calculate",
            type=RouteType.PROTECTED,
            methods=["POST"],
            upstream_service="api",
            rate_limit=1000,
            rate_limit_type=RateLimitType.USER,
            cache_strategy=CacheStrategy.SMART,
            cache_ttl=3600
        ),
        "/api/v1/kundli/analyze": RouteConfig(
            path="/api/v1/kundli/analyze",
            type=RouteType.PROTECTED,
            methods=["POST"],
            upstream_service="api",
            rate_limit=1000,
            rate_limit_type=RateLimitType.USER,
            cache_strategy=CacheStrategy.SMART,
            cache_ttl=3600
        ),
        
        # Admin routes
        "/api/v1/admin/users": RouteConfig(
            path="/api/v1/admin/users",
            type=RouteType.ADMIN,
            methods=["GET", "POST", "PUT", "DELETE"],
            upstream_service="admin",
            roles_required=["admin"],
            rate_limit=100,
            rate_limit_type=RateLimitType.USER
        ),
        "/api/v1/admin/metrics": RouteConfig(
            path="/api/v1/admin/metrics",
            type=RouteType.ADMIN,
            methods=["GET"],
            upstream_service="admin",
            roles_required=["admin"],
            cache_strategy=CacheStrategy.SIMPLE,
            cache_ttl=60
        )
    }
    
    # Service configurations
    if environment == "local":
        services = {
            "api": ServiceConfig(
                name="api",
                hosts=["http://localhost:8000"],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=100,
                ssl_verify=False
            ),
            "auth": ServiceConfig(
                name="auth",
                hosts=["http://localhost:8001"],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=50,
                ssl_verify=False
            ),
            "admin": ServiceConfig(
                name="admin",
                hosts=["http://localhost:8002"],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=20,
                ssl_verify=False
            )
        }
        
        trusted_hosts = ["localhost"]
        cors_origins = ["http://localhost:3000"]
        
    elif environment == "development":
        services = {
            "api": ServiceConfig(
                name="api",
                hosts=[
                    "http://api-1.dev.vedic-astrology.com",
                    "http://api-2.dev.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=200,
                ssl_verify=True
            ),
            "auth": ServiceConfig(
                name="auth",
                hosts=[
                    "http://auth-1.dev.vedic-astrology.com",
                    "http://auth-2.dev.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=100,
                ssl_verify=True
            ),
            "admin": ServiceConfig(
                name="admin",
                hosts=["http://admin.dev.vedic-astrology.com"],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=50,
                ssl_verify=True
            )
        }
        
        trusted_hosts = [".dev.vedic-astrology.com"]
        cors_origins = ["https://dev.vedic-astrology.com"]
        
    elif environment == "staging":
        services = {
            "api": ServiceConfig(
                name="api",
                hosts=[
                    "http://api-1.staging.vedic-astrology.com",
                    "http://api-2.staging.vedic-astrology.com",
                    "http://api-3.staging.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=500,
                ssl_verify=True
            ),
            "auth": ServiceConfig(
                name="auth",
                hosts=[
                    "http://auth-1.staging.vedic-astrology.com",
                    "http://auth-2.staging.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=200,
                ssl_verify=True
            ),
            "admin": ServiceConfig(
                name="admin",
                hosts=[
                    "http://admin-1.staging.vedic-astrology.com",
                    "http://admin-2.staging.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=100,
                ssl_verify=True
            )
        }
        
        trusted_hosts = [".staging.vedic-astrology.com"]
        cors_origins = ["https://staging.vedic-astrology.com"]
        
    else:  # production
        services = {
            "api": ServiceConfig(
                name="api",
                hosts=[
                    "http://api-1.vedic-astrology.com",
                    "http://api-2.vedic-astrology.com",
                    "http://api-3.vedic-astrology.com",
                    "http://api-4.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=1000,
                ssl_verify=True
            ),
            "auth": ServiceConfig(
                name="auth",
                hosts=[
                    "http://auth-1.vedic-astrology.com",
                    "http://auth-2.vedic-astrology.com",
                    "http://auth-3.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=500,
                ssl_verify=True
            ),
            "admin": ServiceConfig(
                name="admin",
                hosts=[
                    "http://admin-1.vedic-astrology.com",
                    "http://admin-2.vedic-astrology.com"
                ],
                health_check_path="/health",
                health_check_interval=30,
                weight=1,
                max_connections=200,
                ssl_verify=True
            )
        }
        
        trusted_hosts = [".vedic-astrology.com"]
        cors_origins = ["https://vedic-astrology.com"]
    
    return GatewayConfig(
        routes=routes,
        services=services,
        load_balance_strategy=LoadBalanceStrategy.ROUND_ROBIN,
        default_timeout=30,
        max_retries=3,
        enable_circuit_breaker=True,
        enable_rate_limiting=True,
        enable_caching=True,
        trusted_hosts=trusted_hosts,
        cors_origins=cors_origins,
        jwt_secret="your-secret-key",  # Should be loaded from environment
        jwt_algorithm="HS256"
    )
