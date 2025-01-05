"""
Zero-Trust Authentication Framework
PGF Protocol: AUTH_001
Gate: GATE_4
Version: 1.0.0
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from enum import Enum
from app.models.user import UserInDB, UserRole
from app.db.repositories.user import UserRepository

class SecurityLevel(str, Enum):
    """Security clearance levels"""
    PUBLIC = "public"         # Public APIs
    BASIC = "basic"          # Basic authenticated access
    ELEVATED = "elevated"    # Elevated privileges
    ADMIN = "admin"          # Administrative access
    SYSTEM = "system"        # System-level access

class TokenType(str, Enum):
    """Token types for different authentication contexts"""
    ACCESS = "access"
    REFRESH = "refresh"
    API = "api"
    SYSTEM = "system"

class AuthToken(BaseModel):
    """Authentication token model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: str

class TokenData(BaseModel):
    """Token payload data"""
    sub: str
    scopes: list[str] = []
    security_level: SecurityLevel
    exp: datetime
    jti: str
    device_id: Optional[str] = None
    ip_address: Optional[str] = None

class AuthConfig:
    """Authentication configuration"""
    SECRET_KEY = "your-secret-key-here"  # Should be loaded from environment
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    # Security settings
    REQUIRE_2FA = True
    MAX_FAILED_ATTEMPTS = 3
    LOCKOUT_DURATION_MINUTES = 15
    PASSWORD_HISTORY_SIZE = 5

    # Role-based security mappings
    ROLE_SECURITY_LEVELS = {
        UserRole.BASIC: SecurityLevel.BASIC,
        UserRole.PREMIUM: SecurityLevel.ELEVATED,
        UserRole.ADMIN: SecurityLevel.ADMIN,
    }

class AuthContext:
    """Authentication context manager"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(
            tokenUrl="token",
            scopes={
                "read": "Read access",
                "write": "Write access",
                "admin": "Admin access"
            }
        )
        self._failed_attempts: Dict[str, int] = {}
        self._lockouts: Dict[str, datetime] = {}
        self._token_blacklist: set = set()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return self.pwd_context.hash(password)
    
    async def create_token(
        self,
        subject: str,
        scopes: list[str],
        security_level: SecurityLevel,
        token_type: TokenType = TokenType.ACCESS,
        device_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuthToken:
        """Create new authentication token"""
        # Determine expiration
        if token_type == TokenType.ACCESS:
            expires_delta = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(days=AuthConfig.REFRESH_TOKEN_EXPIRE_DAYS)

        expire = datetime.utcnow() + expires_delta
        
        # Create token data
        token_data = {
            "sub": subject,
            "scopes": scopes,
            "security_level": security_level,
            "exp": expire,
            "jti": str(datetime.utcnow().timestamp()),
            "type": token_type,
        }
        
        if device_id:
            token_data["device_id"] = device_id
        if ip_address:
            token_data["ip_address"] = ip_address

        # Create tokens
        access_token = jwt.encode(
            token_data,
            AuthConfig.SECRET_KEY,
            algorithm=AuthConfig.ALGORITHM
        )
        
        refresh_token = jwt.encode(
            {**token_data, "type": TokenType.REFRESH},
            AuthConfig.SECRET_KEY,
            algorithm=AuthConfig.ALGORITHM
        )

        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_delta.total_seconds(),
            scope=" ".join(scopes)
        )

    async def verify_token(
        self,
        token: str,
        security_scopes: SecurityScopes,
    ) -> TokenData:
        """Verify and decode token"""
        if token in self._token_blacklist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                token,
                AuthConfig.SECRET_KEY,
                algorithms=[AuthConfig.ALGORITHM]
            )
            token_data = TokenData(**payload)
            
            # Check if token is expired
            if datetime.utcnow() > token_data.exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Verify scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not enough permissions",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

            return token_data

        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
    ) -> UserInDB:
        """Get current authenticated user"""
        token_data = await self.verify_token(token, security_scopes)
        
        user = await UserRepository.get_user_by_id(token_data.sub)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify user has required security level
        user_security_level = AuthConfig.ROLE_SECURITY_LEVELS[user.role]
        if user_security_level.value < token_data.security_level.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    def revoke_token(self, token: str):
        """Add token to blacklist"""
        self._token_blacklist.add(token)

    async def check_rate_limit(self, user_id: str) -> bool:
        """Check if user is rate limited"""
        if user_id in self._lockouts:
            lockout_time = self._lockouts[user_id]
            if datetime.utcnow() < lockout_time:
                return False
            del self._lockouts[user_id]
            self._failed_attempts[user_id] = 0
            
        return True

    def record_failed_attempt(self, user_id: str):
        """Record failed login attempt"""
        self._failed_attempts[user_id] = self._failed_attempts.get(user_id, 0) + 1
        
        if self._failed_attempts[user_id] >= AuthConfig.MAX_FAILED_ATTEMPTS:
            self._lockouts[user_id] = datetime.utcnow() + timedelta(
                minutes=AuthConfig.LOCKOUT_DURATION_MINUTES
            )

# Global authentication context
auth_context = AuthContext()

# Dependency for getting current user
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(auth_context.oauth2_scheme),
) -> UserInDB:
    return await auth_context.get_current_user(security_scopes, token)

# Dependency for getting current active user
async def get_current_active_user(
    current_user: UserInDB = Security(
        get_current_user,
        scopes=["read"],
    ),
) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Dependency for getting current admin user
async def get_current_admin_user(
    current_user: UserInDB = Security(
        get_current_user,
        scopes=["admin"],
    ),
) -> UserInDB:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
