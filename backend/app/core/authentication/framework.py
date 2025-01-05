"""
Service Authentication Framework
PGF Protocol: AUTH_001
Gate: GATE_23
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
from pydantic import BaseModel, Field, EmailStr
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)
from ..service.framework import ServiceTier

class AuthMode(str, Enum):
    """Authentication modes"""
    BASIC = "basic"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    MULTI_FACTOR = "multi_factor"

class AuthScope(str, Enum):
    """Authentication scopes"""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    SYSTEM = "system"

class UserRole(str, Enum):
    """User roles"""
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"
    SYSTEM = "system"

class User(BaseModel):
    """User model"""
    
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False
    role: UserRole = UserRole.USER
    tier: ServiceTier = ServiceTier.BASIC
    scopes: List[AuthScope] = [AuthScope.READ]

class UserInDB(User):
    """User in database"""
    hashed_password: str

class Token(BaseModel):
    """Token model"""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    """Token data"""
    
    username: str
    scopes: List[AuthScope]
    exp: datetime

@dataclass
class AuthenticationMetrics:
    """Authentication metrics"""
    
    login_attempts: int
    failed_attempts: int
    active_sessions: int
    token_refreshes: int
    average_session_duration: float

class AuthenticationManager:
    """Authentication manager"""
    
    def __init__(
        self,
        mode: AuthMode = AuthMode.JWT,
        secret_key: str = "your-secret-key",
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        """Initialize manager"""
        self.mode = mode
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = access_token_expire_minutes
        self.refresh_token_expire = refresh_token_expire_days
        
        # Initialize security
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )
        self.oauth2_scheme = OAuth2PasswordBearer(
            tokenUrl="token"
        )
        
        # Initialize metrics
        self.metrics = AuthenticationMetrics(
            login_attempts=0,
            failed_attempts=0,
            active_sessions=0,
            token_refreshes=0,
            average_session_duration=0.0
        )
        
        # Mock database (replace with real database)
        self.users_db: Dict[str, UserInDB] = {}
    
    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """Verify password"""
        return self.pwd_context.verify(
            plain_password,
            hashed_password
        )
    
    def get_password_hash(
        self,
        password: str
    ) -> str:
        """Get password hash"""
        return self.pwd_context.hash(password)
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        role: UserRole = UserRole.USER,
        tier: ServiceTier = ServiceTier.BASIC,
        scopes: List[AuthScope] = [AuthScope.READ]
    ) -> User:
        """Create new user"""
        if username in self.users_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        user = UserInDB(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            tier=tier,
            scopes=scopes,
            hashed_password=self.get_password_hash(password)
        )
        
        self.users_db[username] = user
        return User(**user.dict(exclude={"hashed_password"}))
    
    def authenticate_user(
        self,
        username: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user"""
        self.metrics.login_attempts += 1
        
        user = self.users_db.get(username)
        if not user:
            self.metrics.failed_attempts += 1
            return None
        
        if not self.verify_password(password, user.hashed_password):
            self.metrics.failed_attempts += 1
            return None
        
        return User(**user.dict(exclude={"hashed_password"}))
    
    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: dict
    ) -> str:
        """Create refresh token"""
        expire = datetime.utcnow() + timedelta(
            days=self.refresh_token_expire
        )
        
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme)
    ) -> User:
        """Get current user from token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            
            token_data = TokenData(
                username=username,
                scopes=payload.get("scopes", []),
                exp=payload.get("exp")
            )
        except jwt.PyJWTError:
            raise credentials_exception
        
        user = self.users_db.get(token_data.username)
        if user is None:
            raise credentials_exception
        
        return User(**user.dict(exclude={"hashed_password"}))
    
    async def get_current_active_user(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current active user"""
        if current_user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
    
    def login(
        self,
        form_data: OAuth2PasswordRequestForm
    ) -> Token:
        """Login user"""
        user = self.authenticate_user(
            form_data.username,
            form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Create access token
        access_token_expires = timedelta(
            minutes=self.access_token_expire
        )
        access_token = self.create_access_token(
            data={
                "sub": user.username,
                "scopes": user.scopes
            },
            expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token = self.create_refresh_token(
            data={
                "sub": user.username,
                "scopes": user.scopes
            }
        )
        
        # Update metrics
        self.metrics.active_sessions += 1
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.access_token_expire * 60,
            refresh_token=refresh_token
        )
    
    def refresh_token(
        self,
        refresh_token: str
    ) -> Token:
        """Refresh access token"""
        try:
            # Verify refresh token
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            # Get user
            user = self.users_db.get(username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            # Create new access token
            access_token_expires = timedelta(
                minutes=self.access_token_expire
            )
            access_token = self.create_access_token(
                data={
                    "sub": user.username,
                    "scopes": user.scopes
                },
                expires_delta=access_token_expires
            )
            
            # Update metrics
            self.metrics.token_refreshes += 1
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.access_token_expire * 60
            )
        
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    
    def logout(
        self,
        current_user: User = Depends(get_current_active_user)
    ):
        """Logout user"""
        # Update metrics
        self.metrics.active_sessions -= 1
        
        # In a real implementation, you would:
        # 1. Invalidate the user's tokens
        # 2. Clear any session data
        # 3. Update the user's last logout time
        pass
