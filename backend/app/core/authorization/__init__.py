"""
Service Authorization Module
PGF Protocol: AUTHZ_003
Gate: GATE_24
Version: 1.0.0
"""

from .framework import (
    AuthorizationMode,
    PolicyEffect,
    ResourceType,
    Action,
    Policy,
    Permission,
    AuthorizationMetrics,
    AuthorizationManager
)
from .config import (
    AUTHORIZATION_CONFIG,
    DEFAULT_POLICIES,
    DEFAULT_PERMISSIONS,
    get_authorization_config
)

__all__ = [
    'AuthorizationMode',
    'PolicyEffect',
    'ResourceType',
    'Action',
    'Policy',
    'Permission',
    'AuthorizationMetrics',
    'AuthorizationManager',
    'AUTHORIZATION_CONFIG',
    'DEFAULT_POLICIES',
    'DEFAULT_PERMISSIONS',
    'get_authorization_config'
]
