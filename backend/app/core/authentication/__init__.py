"""
Service Authentication Module
PGF Protocol: AUTH_003
Gate: GATE_23
Version: 1.0.0
"""

from .framework import (
    AuthMode,
    AuthScope,
    UserRole,
    User,
    UserInDB,
    Token,
    TokenData,
    AuthenticationMetrics,
    AuthenticationManager
)
from .config import (
    AUTH_CONFIG,
    SCOPE_CONFIG,
    ROLE_CONFIG,
    TOKEN_CONFIG,
    SECURITY_CONFIG,
    get_auth_config
)

__all__ = [
    'AuthMode',
    'AuthScope',
    'UserRole',
    'User',
    'UserInDB',
    'Token',
    'TokenData',
    'AuthenticationMetrics',
    'AuthenticationManager',
    'AUTH_CONFIG',
    'SCOPE_CONFIG',
    'ROLE_CONFIG',
    'TOKEN_CONFIG',
    'SECURITY_CONFIG',
    'get_auth_config'
]
