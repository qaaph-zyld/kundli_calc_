"""
Service Scaling Security
PGF Protocol: SCAL_008
Gate: GATE_39
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
import jwt
import hashlib
import logging
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, SecretStr
import json
import os

class SecurityMode(str, Enum):
    """Security modes"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"

class SecurityScope(str, Enum):
    """Security scopes"""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class SecurityAction(str, Enum):
    """Security actions"""
    SCALE = "scale"
    CONFIGURE = "configure"
    MONITOR = "monitor"
    VALIDATE = "validate"

@dataclass
class SecurityAudit:
    """Security audit"""
    
    action: SecurityAction
    timestamp: datetime
    user: str
    status: str
    details: Dict[str, Any]

class SecurityConfig(BaseModel):
    """Security configuration"""
    
    mode: SecurityMode
    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600
    rate_limit: int = 100
    rate_window: int = 60
    allowed_ips: List[str] = []
    allowed_origins: List[str] = []

class ScalingSecurity:
    """Scaling security"""
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        mode: SecurityMode = SecurityMode.STANDARD
    ):
        """Initialize security"""
        self.mode = mode
        self.config_path = config_path
        
        # Initialize configuration
        self._init_config()
        
        # Initialize audit log
        self._init_audit()
        
        # Initialize logger
        self._init_logger()
        
        # Initialize security bearer
        self.security = HTTPBearer()
    
    def _init_config(self):
        """Initialize configuration"""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path) as f:
                config = json.load(f)
        else:
            config = {
                "mode": self.mode,
                "jwt_secret": os.environ.get(
                    "JWT_SECRET",
                    "your-super-secret-key"
                ),
                "jwt_algorithm": "HS256",
                "jwt_expiration": 3600,
                "rate_limit": 100,
                "rate_window": 60,
                "allowed_ips": [],
                "allowed_origins": []
            }
        
        self.config = SecurityConfig(**config)
    
    def _init_audit(self):
        """Initialize audit log"""
        self.audit_log: List[SecurityAudit] = []
    
    def _init_logger(self):
        """Initialize logger"""
        self.logger = logging.getLogger("scaling_security")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(
                "scaling_security.log"
            )
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatters
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            
            # Add formatters
            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)
            
            # Add handlers
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def create_token(
        self,
        user: str,
        scopes: List[SecurityScope]
    ) -> str:
        """Create JWT token"""
        try:
            # Create payload
            payload = {
                "user": user,
                "scopes": [s.value for s in scopes],
                "exp": datetime.utcnow() + timedelta(
                    seconds=self.config.jwt_expiration
                )
            }
            
            # Create token
            token = jwt.encode(
                payload,
                self.config.jwt_secret.get_secret_value(),
                algorithm=self.config.jwt_algorithm
            )
            
            return token
        
        except Exception as e:
            self.logger.error(f"Token creation error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Token creation failed"
            )
    
    def validate_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> Dict[str, Any]:
        """Validate JWT token"""
        try:
            # Decode token
            payload = jwt.decode(
                credentials.credentials,
                self.config.jwt_secret.get_secret_value(),
                algorithms=[self.config.jwt_algorithm]
            )
            
            return payload
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
    
    def validate_scope(
        self,
        token_payload: Dict[str, Any],
        required_scope: SecurityScope
    ):
        """Validate security scope"""
        if (
            required_scope.value not in
            token_payload.get("scopes", [])
        ):
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
    
    def validate_rate_limit(
        self,
        user: str,
        action: SecurityAction
    ):
        """Validate rate limit"""
        # Get recent actions
        recent_actions = [
            a for a in self.audit_log
            if (
                a.user == user and
                a.action == action and
                a.timestamp > datetime.utcnow() -
                timedelta(seconds=self.config.rate_window)
            )
        ]
        
        # Check rate limit
        if len(recent_actions) >= self.config.rate_limit:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
    
    def validate_ip(
        self,
        ip: str
    ):
        """Validate IP address"""
        if (
            self.config.allowed_ips and
            ip not in self.config.allowed_ips
        ):
            raise HTTPException(
                status_code=403,
                detail="IP not allowed"
            )
    
    def validate_origin(
        self,
        origin: str
    ):
        """Validate origin"""
        if (
            self.config.allowed_origins and
            origin not in self.config.allowed_origins
        ):
            raise HTTPException(
                status_code=403,
                detail="Origin not allowed"
            )
    
    def audit_action(
        self,
        action: SecurityAction,
        user: str,
        status: str,
        details: Dict[str, Any]
    ):
        """Audit security action"""
        try:
            # Create audit entry
            audit = SecurityAudit(
                action=action,
                timestamp=datetime.utcnow(),
                user=user,
                status=status,
                details=details
            )
            
            # Add to audit log
            self.audit_log.append(audit)
            
            # Log action
            self.logger.info(
                f"Security audit: {action.value} by {user}"
            )
        
        except Exception as e:
            self.logger.error(f"Audit error: {str(e)}")
    
    def hash_secret(
        self,
        secret: str
    ) -> str:
        """Hash secret value"""
        return hashlib.sha256(
            secret.encode()
        ).hexdigest()
    
    def rotate_secret(self):
        """Rotate JWT secret"""
        try:
            # Generate new secret
            new_secret = os.urandom(32).hex()
            
            # Update configuration
            self.config.jwt_secret = SecretStr(new_secret)
            
            # Save configuration
            if self.config_path:
                config_dict = self.config.dict()
                config_dict["jwt_secret"] = new_secret
                
                with open(self.config_path, "w") as f:
                    json.dump(config_dict, f, indent=4)
            
            self.logger.info("Secret rotation completed")
        
        except Exception as e:
            self.logger.error(f"Secret rotation error: {str(e)}")
            raise e
    
    def get_audit_log(
        self,
        user: Optional[str] = None,
        action: Optional[SecurityAction] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[SecurityAudit]:
        """Get audit log entries"""
        filtered_log = self.audit_log
        
        # Filter by user
        if user:
            filtered_log = [
                a for a in filtered_log
                if a.user == user
            ]
        
        # Filter by action
        if action:
            filtered_log = [
                a for a in filtered_log
                if a.action == action
            ]
        
        # Filter by time range
        if start_time:
            filtered_log = [
                a for a in filtered_log
                if a.timestamp >= start_time
            ]
        
        if end_time:
            filtered_log = [
                a for a in filtered_log
                if a.timestamp <= end_time
            ]
        
        return filtered_log
