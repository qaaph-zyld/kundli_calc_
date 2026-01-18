"""
Rate Limiting Middleware
========================
Implements rate limiting using slowapi to prevent API abuse.
"""

import os
from typing import Callable

from fastapi import Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute"],  # Default: 60 requests per minute per IP
    enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
)


def get_rate_limit_config():
    """Get rate limiting configuration from environment"""
    return {
        "enabled": os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
        "per_minute": int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
        "per_hour": int(os.getenv("RATE_LIMIT_PER_HOUR", "1000")),
        "burst": int(os.getenv("RATE_LIMIT_BURST", "10")),
    }


# Rate limit decorators for different endpoint types
def rate_limit_standard(func):
    """Standard rate limit: 60/minute"""
    return limiter.limit("60/minute")(func)


def rate_limit_strict(func):
    """Strict rate limit: 20/minute (for heavy computations)"""
    return limiter.limit("20/minute")(func)


def rate_limit_relaxed(func):
    """Relaxed rate limit: 120/minute (for lightweight reads)"""
    return limiter.limit("120/minute")(func)


def rate_limit_calculation(func):
    """Rate limit for calculation-heavy endpoints: 30/minute"""
    return limiter.limit("30/minute")(func)


async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to add rate limiting headers to all responses
    """
    response = await call_next(request)

    # Add rate limit headers for transparency
    config = get_rate_limit_config()
    if config["enabled"]:
        response.headers["X-RateLimit-Limit"] = str(config["per_minute"])
        response.headers["X-RateLimit-Remaining"] = "Unknown"  # slowapi tracks this
        response.headers["X-RateLimit-Reset"] = "60"  # seconds until reset

    return response


def setup_rate_limiting(app):
    """
    Setup rate limiting for FastAPI application

    Args:
        app: FastAPI application instance
    """
    from fastapi import FastAPI

    # Add rate limiter to app state
    app.state.limiter = limiter

    # Add exception handler for rate limit exceeded
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add middleware for rate limit headers
    app.middleware("http")(rate_limit_middleware)

    return app
