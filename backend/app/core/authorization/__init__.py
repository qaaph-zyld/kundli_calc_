"""
Service Authorization Module
PGF Protocol: AUTHZ_003
Gate: GATE_24
Version: 1.0.0
"""

from .config import AUTHORIZATION_CONFIG, DEFAULT_PERMISSIONS, DEFAULT_POLICIES, get_authorization_config
from .framework import (
    Action,
    AuthorizationManager,
    AuthorizationMetrics,
    AuthorizationMode,
    Permission,
    Policy,
    PolicyEffect,
    ResourceType,
)

__all__ = [
    "AuthorizationMode",
    "PolicyEffect",
    "ResourceType",
    "Action",
    "Policy",
    "Permission",
    "AuthorizationMetrics",
    "AuthorizationManager",
    "AUTHORIZATION_CONFIG",
    "DEFAULT_POLICIES",
    "DEFAULT_PERMISSIONS",
    "get_authorization_config",
]
