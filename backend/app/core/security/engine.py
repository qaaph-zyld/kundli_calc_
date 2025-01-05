"""
Enhanced Security Engine for Kundli Calculation Service
Implements JWT authentication, rate limiting, and RBAC
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.core.config.settings import settings
from app.core.cache import RedisCache
from app.core.models.user import User

class SecurityScope(BaseModel):
    """Security scope model"""
    name: str
    permissions: List[str]

class TokenData(BaseModel):
    """Token data model"""
    username: str
    scopes: List[SecurityScope]
    exp: datetime

class SecurityEngine:
    """Enhanced security engine with rate limiting and RBAC"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.redis_cache = RedisCache()
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
        
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return self.pwd_context.hash(password)
        
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token with enhanced security"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """Get current user from JWT token with rate limiting"""
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Rate limiting check
        if not await self.check_rate_limit(token):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
            
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
                
            token_data = TokenData(
                username=username,
                scopes=payload.get("scopes", []),
                exp=datetime.fromtimestamp(payload.get("exp"))
            )
        except JWTError:
            raise credentials_exception
            
        user = await self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
            
        return user
        
    async def check_rate_limit(self, token: str) -> bool:
        """Check rate limiting for the token"""
        key = f"rate_limit:{token}"
        current_count = await self.redis_cache.get(key) or 0
        
        if current_count >= settings.RATE_LIMIT_MAX_REQUESTS:
            return False
            
        await self.redis_cache.incr(key)
        await self.redis_cache.expire(key, settings.RATE_LIMIT_WINDOW_SECONDS)
        return True
        
    async def verify_scope(self, user: User, required_scope: SecurityScope) -> bool:
        """Verify user has required scope"""
        user_scopes = await self.get_user_scopes(user)
        return any(
            scope.name == required_scope.name and
            all(perm in scope.permissions for perm in required_scope.permissions)
            for scope in user_scopes
        )
        
    async def get_user_scopes(self, user: User) -> List[SecurityScope]:
        """Get user scopes from cache or database"""
        cache_key = f"user_scopes:{user.id}"
        cached_scopes = await self.redis_cache.get(cache_key)
        
        if cached_scopes:
            return [SecurityScope(**scope) for scope in cached_scopes]
            
        # Get from database and cache
        scopes = await self.load_user_scopes(user)
        await self.redis_cache.set(
            cache_key,
            [scope.dict() for scope in scopes],
            expire=settings.CACHE_TTL_SECONDS
        )
        return scopes
        
    async def load_user_scopes(self, user: User) -> List[SecurityScope]:
        """Load user scopes from database"""
        # Implement database loading logic here
        return []
        
    async def get_user(self, username: str) -> Optional[User]:
        """Get user from database"""
        # Implement database user loading logic here
        return None

security_engine = SecurityEngine()
