from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str]
    role: UserRole = UserRole.BASIC
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    password: Optional[str]
    role: Optional[UserRole]
    status: Optional[UserStatus]

class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime]
    saved_kundlis: List[str] = []  # List of kundli IDs

class UserResponse(UserBase):
    id: str
    created_at: datetime
    last_login: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    refresh_token: str

class TokenData(BaseModel):
    user_id: str
    role: UserRole
    exp: datetime

class RefreshToken(BaseModel):
    refresh_token: str
