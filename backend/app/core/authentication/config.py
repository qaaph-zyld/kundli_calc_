"""
Service Authentication Configuration
PGF Protocol: AUTH_002
Gate: GATE_23
Version: 1.0.0
"""

from typing import Dict, Any, List
from .framework import (
    AuthMode,
    AuthScope,
    UserRole
)

# Authentication configuration
AUTH_CONFIG = {
    AuthMode.BASIC: {
        "enabled": True,
        "token_required": False,
        "session_management": False,
        "password_hashing": True,
        "rate_limiting": True
    },
    AuthMode.OAUTH2: {
        "enabled": True,
        "token_required": True,
        "session_management": True,
        "password_hashing": True,
        "rate_limiting": True,
        "refresh_tokens": True
    },
    AuthMode.JWT: {
        "enabled": True,
        "token_required": True,
        "session_management": False,
        "password_hashing": True,
        "rate_limiting": True,
        "refresh_tokens": True
    },
    AuthMode.MULTI_FACTOR: {
        "enabled": True,
        "token_required": True,
        "session_management": True,
        "password_hashing": True,
        "rate_limiting": True,
        "refresh_tokens": True,
        "mfa_required": True
    }
}

# Scope configuration
SCOPE_CONFIG = {
    AuthScope.READ: {
        "enabled": True,
        "endpoints": [
            "GET /chart",
            "GET /transit",
            "GET /progression"
        ],
        "rate_limit": 100,
        "requires_verification": False
    },
    AuthScope.WRITE: {
        "enabled": True,
        "endpoints": [
            "POST /chart",
            "POST /transit",
            "POST /progression"
        ],
        "rate_limit": 50,
        "requires_verification": True
    },
    AuthScope.ADMIN: {
        "enabled": True,
        "endpoints": [
            "*"
        ],
        "rate_limit": 1000,
        "requires_verification": True
    },
    AuthScope.SYSTEM: {
        "enabled": True,
        "endpoints": [
            "*"
        ],
        "rate_limit": None,
        "requires_verification": True
    }
}

# Role configuration
ROLE_CONFIG = {
    UserRole.USER: {
        "enabled": True,
        "scopes": [
            AuthScope.READ
        ],
        "max_requests": 1000,
        "requires_verification": False
    },
    UserRole.PREMIUM: {
        "enabled": True,
        "scopes": [
            AuthScope.READ,
            AuthScope.WRITE
        ],
        "max_requests": 10000,
        "requires_verification": True
    },
    UserRole.ADMIN: {
        "enabled": True,
        "scopes": [
            AuthScope.READ,
            AuthScope.WRITE,
            AuthScope.ADMIN
        ],
        "max_requests": None,
        "requires_verification": True
    },
    UserRole.SYSTEM: {
        "enabled": True,
        "scopes": [
            AuthScope.READ,
            AuthScope.WRITE,
            AuthScope.ADMIN,
            AuthScope.SYSTEM
        ],
        "max_requests": None,
        "requires_verification": True
    }
}

# Token configuration
TOKEN_CONFIG = {
    "algorithm": "HS256",
    "access_token": {
        "expire_minutes": 30,
        "secret_key": "your-secret-key",
        "auto_refresh": True
    },
    "refresh_token": {
        "expire_days": 7,
        "secret_key": "your-refresh-secret-key",
        "reuse_detection": True
    }
}

# Security configuration
SECURITY_CONFIG = {
    "password": {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special": True,
        "max_age_days": 90
    },
    "session": {
        "max_active": 5,
        "idle_timeout": 1800,
        "absolute_timeout": 43200
    },
    "rate_limiting": {
        "enabled": True,
        "window_size": 3600,
        "max_requests": 1000
    },
    "mfa": {
        "enabled": True,
        "methods": ["totp", "email"],
        "grace_period": 7
    }
}

def get_auth_config(environment: str) -> Dict[str, Any]:
    """Get authentication configuration for environment"""
    
    base_config = {
        "auth_config": AUTH_CONFIG,
        "scope_config": SCOPE_CONFIG,
        "role_config": ROLE_CONFIG,
        "token_config": TOKEN_CONFIG,
        "security_config": SECURITY_CONFIG
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["auth_config"] = {
            AuthMode.BASIC: AUTH_CONFIG[AuthMode.BASIC]
        }
        base_config["scope_config"] = {
            AuthScope.READ: SCOPE_CONFIG[AuthScope.READ]
        }
        base_config["security_config"]["password"].update({
            "min_length": 4,
            "require_uppercase": False,
            "require_special": False
        })
        base_config["security_config"]["mfa"]["enabled"] = False
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["auth_config"][AuthMode.JWT].update({
            "debug_mode": True,
            "log_tokens": True
        })
        base_config["security_config"]["rate_limiting"]["max_requests"] = 10000
    
    else:  # staging and production
        # Full configuration with enhanced security
        base_config["security_config"].update({
            "ip_whitelist": True,
            "audit_logging": True
        })
        base_config["token_config"]["access_token"]["expire_minutes"] = 15
    
    return base_config
