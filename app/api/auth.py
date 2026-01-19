from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.rate_limiter import rate_limit
from app.schema.auth import LoginRequest, TokenResponse, RegisterRequest
from app.services.user_service import authenticate_user, get_user_by_username, create_user
from app.core.security import create_access_token, create_refresh_token
from app.core.dependencies import get_db

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    key = f"rate:login:{data.username}"

    if not rate_limit(key, limit=5, window_seconds=60):
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try later."
        )

    user = authenticate_user(db, data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    refreshToken=create_refresh_token({"sub": user.username})
    return TokenResponse(access_token=token, refresh_token=refreshToken)



@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, data.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = create_user(db, data.username, data.password)

    from app.core.security import create_access_token

    token = create_access_token({"sub": user.username})

    refreshToken=create_refresh_token({"sub": user.username})
    return TokenResponse(access_token=token, refresh_token=refreshToken)

