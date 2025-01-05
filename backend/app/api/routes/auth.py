from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from app.models.user import (
    UserCreate,
    UserResponse,
    Token,
    RefreshToken,
    UserInDB,
)
from app.db.repositories.user import UserRepository

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    # Check if user already exists
    if await UserRepository.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    if await UserRepository.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    user_in_db = UserInDB(
        **user_data.dict(exclude={"password"}),
        hashed_password=hashed_password,
    )
    
    created_user = await UserRepository.create_user(user_in_db)
    return UserResponse(**created_user.dict())

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserRepository.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    await UserRepository.update_last_login(user.id)

    # Create tokens
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)
    
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role},
        expires_delta=access_token_expires,
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds(),
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token: RefreshToken):
    try:
        # Verify refresh token and get user
        user = await get_current_user(token.refresh_token)
        
        # Create new tokens
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=7)
        
        access_token = create_access_token(
            data={"sub": user.id, "role": user.role},
            expires_delta=access_token_expires,
        )
        
        refresh_token = create_refresh_token(
            data={"sub": user.id},
            expires_delta=refresh_token_expires,
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=access_token_expires.total_seconds(),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_user)
):
    return UserResponse(**current_user.dict())
