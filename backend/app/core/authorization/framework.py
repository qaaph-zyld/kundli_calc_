"""
Service Authorization Framework
PGF Protocol: AUTHZ_001
Gate: GATE_24
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set, Callable
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)
from ..authentication.framework import (
    User,
    AuthScope,
    UserRole,
    AuthenticationManager
)
from ..service.framework import ServiceTier

class AuthorizationMode(str, Enum):
    """Authorization modes"""
    ROLE_BASED = "role_based"
    SCOPE_BASED = "scope_based"
    POLICY_BASED = "policy_based"
    ATTRIBUTE_BASED = "attribute_based"

class PolicyEffect(str, Enum):
    """Policy effects"""
    ALLOW = "allow"
    DENY = "deny"

class ResourceType(str, Enum):
    """Resource types"""
    CHART = "chart"
    TRANSIT = "transit"
    PROGRESSION = "progression"
    COMPATIBILITY = "compatibility"
    PREDICTION = "prediction"

class Action(str, Enum):
    """Resource actions"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"

class Policy(BaseModel):
    """Authorization policy"""
    
    name: str
    effect: PolicyEffect
    roles: List[UserRole]
    resources: List[ResourceType]
    actions: List[Action]
    conditions: Optional[Dict[str, Any]] = None

class Permission(BaseModel):
    """Resource permission"""
    
    resource: ResourceType
    actions: List[Action]
    scopes: List[AuthScope]

@dataclass
class AuthorizationMetrics:
    """Authorization metrics"""
    
    policy_evaluations: int
    allowed_requests: int
    denied_requests: int
    cache_hits: int
    average_evaluation_time: float

class AuthorizationManager:
    """Authorization manager"""
    
    def __init__(
        self,
        mode: AuthorizationMode = AuthorizationMode.POLICY_BASED,
        auth_manager: AuthenticationManager = None,
        enable_caching: bool = True
    ):
        """Initialize manager"""
        self.mode = mode
        self.auth_manager = auth_manager
        self.enable_caching = enable_caching
        
        # Initialize policies
        self.policies: Dict[str, Policy] = {}
        
        # Initialize permissions
        self.permissions: Dict[UserRole, List[Permission]] = {}
        
        # Initialize metrics
        self.metrics = AuthorizationMetrics(
            policy_evaluations=0,
            allowed_requests=0,
            denied_requests=0,
            cache_hits=0,
            average_evaluation_time=0.0
        )
        
        # Initialize cache
        self.policy_cache: Dict[str, bool] = {}
    
    def add_policy(self, policy: Policy):
        """Add authorization policy"""
        self.policies[policy.name] = policy
        
        # Clear cache
        if self.enable_caching:
            self.policy_cache.clear()
    
    def remove_policy(self, policy_name: str):
        """Remove authorization policy"""
        if policy_name in self.policies:
            del self.policies[policy_name]
            
            # Clear cache
            if self.enable_caching:
                self.policy_cache.clear()
    
    def add_permission(
        self,
        role: UserRole,
        permission: Permission
    ):
        """Add role permission"""
        if role not in self.permissions:
            self.permissions[role] = []
        self.permissions[role].append(permission)
    
    def remove_permission(
        self,
        role: UserRole,
        resource: ResourceType
    ):
        """Remove role permission"""
        if role in self.permissions:
            self.permissions[role] = [
                p for p in self.permissions[role]
                if p.resource != resource
            ]
    
    async def authorize(
        self,
        user: User,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Authorize user action"""
        start_time = datetime.now()
        self.metrics.policy_evaluations += 1
        
        # Check cache
        cache_key = f"{user.username}:{resource}:{action}"
        if self.enable_caching and cache_key in self.policy_cache:
            self.metrics.cache_hits += 1
            return self.policy_cache[cache_key]
        
        authorized = False
        
        if self.mode == AuthorizationMode.ROLE_BASED:
            authorized = self._check_role_permissions(
                user.role,
                resource,
                action
            )
        
        elif self.mode == AuthorizationMode.SCOPE_BASED:
            authorized = self._check_scope_permissions(
                user.scopes,
                resource,
                action
            )
        
        elif self.mode == AuthorizationMode.POLICY_BASED:
            authorized = self._evaluate_policies(
                user,
                resource,
                action
            )
        
        elif self.mode == AuthorizationMode.ATTRIBUTE_BASED:
            authorized = self._check_attributes(
                user,
                resource,
                action
            )
        
        # Update metrics
        end_time = datetime.now()
        evaluation_time = (
            end_time - start_time
        ).total_seconds()
        
        self.metrics.average_evaluation_time = (
            self.metrics.average_evaluation_time *
            (self.metrics.policy_evaluations - 1) +
            evaluation_time
        ) / self.metrics.policy_evaluations
        
        if authorized:
            self.metrics.allowed_requests += 1
        else:
            self.metrics.denied_requests += 1
        
        # Update cache
        if self.enable_caching:
            self.policy_cache[cache_key] = authorized
        
        return authorized
    
    def _check_role_permissions(
        self,
        role: UserRole,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Check role-based permissions"""
        if role not in self.permissions:
            return False
        
        for permission in self.permissions[role]:
            if (
                permission.resource == resource and
                action in permission.actions
            ):
                return True
        
        return False
    
    def _check_scope_permissions(
        self,
        scopes: List[AuthScope],
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Check scope-based permissions"""
        required_scopes = self._get_required_scopes(
            resource,
            action
        )
        
        return all(
            scope in scopes
            for scope in required_scopes
        )
    
    def _evaluate_policies(
        self,
        user: User,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Evaluate authorization policies"""
        for policy in self.policies.values():
            if (
                user.role in policy.roles and
                resource in policy.resources and
                action in policy.actions
            ):
                if policy.conditions:
                    if self._evaluate_conditions(
                        user,
                        policy.conditions
                    ):
                        return policy.effect == PolicyEffect.ALLOW
                else:
                    return policy.effect == PolicyEffect.ALLOW
        
        return False
    
    def _check_attributes(
        self,
        user: User,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Check attribute-based permissions"""
        # Check service tier
        if not self._check_tier_permissions(
            user.tier,
            resource,
            action
        ):
            return False
        
        # Check user attributes
        if not self._check_user_attributes(
            user,
            resource,
            action
        ):
            return False
        
        return True
    
    def _get_required_scopes(
        self,
        resource: ResourceType,
        action: Action
    ) -> List[AuthScope]:
        """Get required scopes for action"""
        if action == Action.READ:
            return [AuthScope.READ]
        elif action in [Action.CREATE, Action.UPDATE, Action.DELETE]:
            return [AuthScope.WRITE]
        elif action == Action.EXECUTE:
            return [AuthScope.ADMIN]
        return []
    
    def _evaluate_conditions(
        self,
        user: User,
        conditions: Dict[str, Any]
    ) -> bool:
        """Evaluate policy conditions"""
        for key, value in conditions.items():
            if key == "time_range":
                if not self._check_time_range(
                    value["start"],
                    value["end"]
                ):
                    return False
            elif key == "request_limit":
                if not self._check_request_limit(
                    user,
                    value
                ):
                    return False
            elif key == "ip_range":
                if not self._check_ip_range(
                    value
                ):
                    return False
        return True
    
    def _check_tier_permissions(
        self,
        tier: ServiceTier,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Check service tier permissions"""
        if tier == ServiceTier.BASIC:
            return resource in [
                ResourceType.CHART,
                ResourceType.TRANSIT
            ]
        elif tier == ServiceTier.STANDARD:
            return resource in [
                ResourceType.CHART,
                ResourceType.TRANSIT,
                ResourceType.PROGRESSION
            ]
        elif tier == ServiceTier.PREMIUM:
            return resource in [
                ResourceType.CHART,
                ResourceType.TRANSIT,
                ResourceType.PROGRESSION,
                ResourceType.COMPATIBILITY
            ]
        elif tier == ServiceTier.ENTERPRISE:
            return True
        return False
    
    def _check_user_attributes(
        self,
        user: User,
        resource: ResourceType,
        action: Action
    ) -> bool:
        """Check user attributes"""
        # Check if user is disabled
        if user.disabled:
            return False
        
        # Check if user has required role
        if resource == ResourceType.PREDICTION:
            return user.role in [
                UserRole.ADMIN,
                UserRole.SYSTEM
            ]
        
        return True
    
    def _check_time_range(
        self,
        start: datetime,
        end: datetime
    ) -> bool:
        """Check if current time is within range"""
        now = datetime.utcnow()
        return start <= now <= end
    
    def _check_request_limit(
        self,
        user: User,
        limit: int
    ) -> bool:
        """Check if user is within request limit"""
        # In a real implementation, you would:
        # 1. Track user requests in a database
        # 2. Check against the limit
        # 3. Update the request count
        return True
    
    def _check_ip_range(
        self,
        allowed_ips: List[str]
    ) -> bool:
        """Check if client IP is allowed"""
        # In a real implementation, you would:
        # 1. Get the client IP from the request
        # 2. Check if it's in the allowed range
        return True
