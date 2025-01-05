"""
Service Authorization Configuration
PGF Protocol: AUTHZ_002
Gate: GATE_24
Version: 1.0.0
"""

from typing import Dict, Any, List
from ..authentication.framework import (
    UserRole,
    AuthScope
)
from .framework import (
    AuthorizationMode,
    PolicyEffect,
    ResourceType,
    Action,
    Policy,
    Permission
)

# Authorization configuration
AUTHORIZATION_CONFIG = {
    AuthorizationMode.ROLE_BASED: {
        "enabled": True,
        "hierarchical": True,
        "inheritance": True,
        "default_deny": True
    },
    AuthorizationMode.SCOPE_BASED: {
        "enabled": True,
        "hierarchical": False,
        "inheritance": False,
        "default_deny": True
    },
    AuthorizationMode.POLICY_BASED: {
        "enabled": True,
        "hierarchical": True,
        "inheritance": True,
        "default_deny": True,
        "policy_combining": "deny_overrides"
    },
    AuthorizationMode.ATTRIBUTE_BASED: {
        "enabled": True,
        "hierarchical": False,
        "inheritance": False,
        "default_deny": True,
        "attribute_combining": "deny_overrides"
    }
}

# Default policies
DEFAULT_POLICIES = {
    "basic_user_policy": Policy(
        name="basic_user_policy",
        effect=PolicyEffect.ALLOW,
        roles=[UserRole.USER],
        resources=[
            ResourceType.CHART,
            ResourceType.TRANSIT
        ],
        actions=[
            Action.READ,
            Action.CREATE
        ],
        conditions={
            "request_limit": 100,
            "time_range": {
                "start": "00:00:00",
                "end": "23:59:59"
            }
        }
    ),
    "premium_user_policy": Policy(
        name="premium_user_policy",
        effect=PolicyEffect.ALLOW,
        roles=[UserRole.PREMIUM],
        resources=[
            ResourceType.CHART,
            ResourceType.TRANSIT,
            ResourceType.PROGRESSION,
            ResourceType.COMPATIBILITY
        ],
        actions=[
            Action.READ,
            Action.CREATE,
            Action.UPDATE
        ],
        conditions={
            "request_limit": 1000,
            "time_range": {
                "start": "00:00:00",
                "end": "23:59:59"
            }
        }
    ),
    "admin_policy": Policy(
        name="admin_policy",
        effect=PolicyEffect.ALLOW,
        roles=[UserRole.ADMIN],
        resources=[
            ResourceType.CHART,
            ResourceType.TRANSIT,
            ResourceType.PROGRESSION,
            ResourceType.COMPATIBILITY,
            ResourceType.PREDICTION
        ],
        actions=[
            Action.READ,
            Action.CREATE,
            Action.UPDATE,
            Action.DELETE,
            Action.EXECUTE
        ],
        conditions=None
    ),
    "system_policy": Policy(
        name="system_policy",
        effect=PolicyEffect.ALLOW,
        roles=[UserRole.SYSTEM],
        resources=[
            ResourceType.CHART,
            ResourceType.TRANSIT,
            ResourceType.PROGRESSION,
            ResourceType.COMPATIBILITY,
            ResourceType.PREDICTION
        ],
        actions=[
            Action.READ,
            Action.CREATE,
            Action.UPDATE,
            Action.DELETE,
            Action.EXECUTE
        ],
        conditions=None
    )
}

# Default permissions
DEFAULT_PERMISSIONS = {
    UserRole.USER: [
        Permission(
            resource=ResourceType.CHART,
            actions=[Action.READ, Action.CREATE],
            scopes=[AuthScope.READ]
        ),
        Permission(
            resource=ResourceType.TRANSIT,
            actions=[Action.READ, Action.CREATE],
            scopes=[AuthScope.READ]
        )
    ],
    UserRole.PREMIUM: [
        Permission(
            resource=ResourceType.CHART,
            actions=[Action.READ, Action.CREATE, Action.UPDATE],
            scopes=[AuthScope.READ, AuthScope.WRITE]
        ),
        Permission(
            resource=ResourceType.TRANSIT,
            actions=[Action.READ, Action.CREATE, Action.UPDATE],
            scopes=[AuthScope.READ, AuthScope.WRITE]
        ),
        Permission(
            resource=ResourceType.PROGRESSION,
            actions=[Action.READ, Action.CREATE],
            scopes=[AuthScope.READ, AuthScope.WRITE]
        ),
        Permission(
            resource=ResourceType.COMPATIBILITY,
            actions=[Action.READ, Action.CREATE],
            scopes=[AuthScope.READ, AuthScope.WRITE]
        )
    ],
    UserRole.ADMIN: [
        Permission(
            resource=ResourceType.CHART,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN
            ]
        ),
        Permission(
            resource=ResourceType.TRANSIT,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN
            ]
        ),
        Permission(
            resource=ResourceType.PROGRESSION,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN
            ]
        ),
        Permission(
            resource=ResourceType.COMPATIBILITY,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN
            ]
        ),
        Permission(
            resource=ResourceType.PREDICTION,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN
            ]
        )
    ],
    UserRole.SYSTEM: [
        Permission(
            resource=ResourceType.CHART,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN,
                AuthScope.SYSTEM
            ]
        ),
        Permission(
            resource=ResourceType.TRANSIT,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN,
                AuthScope.SYSTEM
            ]
        ),
        Permission(
            resource=ResourceType.PROGRESSION,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN,
                AuthScope.SYSTEM
            ]
        ),
        Permission(
            resource=ResourceType.COMPATIBILITY,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN,
                AuthScope.SYSTEM
            ]
        ),
        Permission(
            resource=ResourceType.PREDICTION,
            actions=[
                Action.READ,
                Action.CREATE,
                Action.UPDATE,
                Action.DELETE,
                Action.EXECUTE
            ],
            scopes=[
                AuthScope.READ,
                AuthScope.WRITE,
                AuthScope.ADMIN,
                AuthScope.SYSTEM
            ]
        )
    ]
}

def get_authorization_config(environment: str) -> Dict[str, Any]:
    """Get authorization configuration for environment"""
    
    base_config = {
        "authorization_config": AUTHORIZATION_CONFIG,
        "default_policies": DEFAULT_POLICIES,
        "default_permissions": DEFAULT_PERMISSIONS
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["authorization_config"] = {
            AuthorizationMode.ROLE_BASED: AUTHORIZATION_CONFIG[AuthorizationMode.ROLE_BASED]
        }
        base_config["default_policies"] = {
            "basic_user_policy": DEFAULT_POLICIES["basic_user_policy"]
        }
        base_config["default_permissions"] = {
            UserRole.USER: DEFAULT_PERMISSIONS[UserRole.USER]
        }
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["authorization_config"][AuthorizationMode.POLICY_BASED].update({
            "debug_mode": True,
            "log_decisions": True
        })
    
    else:  # staging and production
        # Full configuration with enhanced security
        base_config["authorization_config"].update({
            "audit_logging": True,
            "decision_caching": True
        })
    
    return base_config
