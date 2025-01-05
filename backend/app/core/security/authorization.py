"""
Authorization Framework
PGF Protocol: SECURITY_002
Gate: GATE_5
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Set, Union
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from .engine import SecurityScope, security_engine

class ResourceType(str, Enum):
    """Resource types"""
    KUNDLI = "kundli"
    PATTERN = "pattern"
    USER = "user"
    SYSTEM = "system"

class Permission(str, Enum):
    """Permission types"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"

class Role(str, Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    SYSTEM = "system"

class Policy(BaseModel):
    """Access policy"""
    
    name: str
    description: Optional[str] = None
    role: Role
    resource_type: ResourceType
    permissions: Set[Permission]
    conditions: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AuthorizationManager:
    """Authorization manager for access control"""
    
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default access policies"""
        # Admin policies
        self.add_policy(Policy(
            name="admin_full_access",
            description="Full access for administrators",
            role=Role.ADMIN,
            resource_type=ResourceType.SYSTEM,
            permissions={
                Permission.CREATE,
                Permission.READ,
                Permission.UPDATE,
                Permission.DELETE,
                Permission.EXECUTE,
                Permission.ADMIN
            }
        ))
        
        # User policies
        self.add_policy(Policy(
            name="user_kundli_access",
            description="Kundli access for regular users",
            role=Role.USER,
            resource_type=ResourceType.KUNDLI,
            permissions={
                Permission.CREATE,
                Permission.READ,
                Permission.UPDATE,
                Permission.DELETE
            }
        ))
        
        self.add_policy(Policy(
            name="user_pattern_access",
            description="Pattern access for regular users",
            role=Role.USER,
            resource_type=ResourceType.PATTERN,
            permissions={
                Permission.CREATE,
                Permission.READ
            }
        ))
        
        # Guest policies
        self.add_policy(Policy(
            name="guest_read_access",
            description="Read-only access for guests",
            role=Role.GUEST,
            resource_type=ResourceType.KUNDLI,
            permissions={Permission.READ}
        ))
        
        # System policies
        self.add_policy(Policy(
            name="system_execution",
            description="System execution permissions",
            role=Role.SYSTEM,
            resource_type=ResourceType.SYSTEM,
            permissions={Permission.EXECUTE}
        ))
    
    def add_policy(self, policy: Policy) -> None:
        """Add new access policy"""
        self.policies[policy.name] = policy
    
    def remove_policy(self, policy_name: str) -> None:
        """Remove access policy"""
        self.policies.pop(policy_name, None)
    
    def get_policy(self, policy_name: str) -> Optional[Policy]:
        """Get access policy by name"""
        return self.policies.get(policy_name)
    
    def get_policies_by_role(self, role: Role) -> List[Policy]:
        """Get all policies for a role"""
        return [
            policy for policy in self.policies.values()
            if policy.role == role
        ]
    
    def has_permission(
        self,
        role: Role,
        resource_type: ResourceType,
        permission: Permission,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if role has permission for resource"""
        policies = self.get_policies_by_role(role)
        
        for policy in policies:
            if (policy.resource_type == resource_type and
                permission in policy.permissions):
                
                # Check conditions if present
                if policy.conditions and context:
                    if not self._evaluate_conditions(policy.conditions, context):
                        continue
                
                return True
        
        return False
    
    def _evaluate_conditions(
        self,
        conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate policy conditions against context"""
        for key, value in conditions.items():
            if key not in context:
                return False
                
            if isinstance(value, (str, int, float, bool)):
                if context[key] != value:
                    return False
            elif isinstance(value, list):
                if context[key] not in value:
                    return False
            elif isinstance(value, dict):
                if not isinstance(context[key], dict):
                    return False
                if not self._evaluate_conditions(value, context[key]):
                    return False
        
        return True
    
    def get_user_permissions(
        self,
        role: Role,
        resource_type: ResourceType
    ) -> Set[Permission]:
        """Get all permissions for a role on a resource"""
        policies = self.get_policies_by_role(role)
        permissions = set()
        
        for policy in policies:
            if policy.resource_type == resource_type:
                permissions.update(policy.permissions)
        
        return permissions

# Global authorization manager instance
authorization_manager = AuthorizationManager()
