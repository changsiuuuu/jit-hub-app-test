import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from ..database import get_db
from ..models import User, ApiKey
from ..schemas import (
    SignupRequest, LoginRequest, TokenResponse,
    UserResponse, ApiKeyCreate, ApiKeyResponse,
)
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user


@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=pwd_context.hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_token(user.id))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    return TokenResponse(access_token=create_token(user.id))


@router.get("/me", response_model=UserResponse)
def me(token: str, db: Session = Depends(get_db)):
    return get_current_user(token, db)


@router.post("/apikey", response_model=ApiKeyResponse, status_code=201)
def create_apikey(payload: ApiKeyCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    new_key = ApiKey(
        user_id=user.id,
        key_name=payload.key_name,
        api_type=payload.api_type,
        key=f"jithub-{uuid.uuid4().hex[:8]}-3meal-api-key",
        status="[활성]",
        is_active=True,
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return new_key


@router.get("/apikey", response_model=list[ApiKeyResponse])
def get_apikeys(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return db.query(ApiKey).filter(ApiKey.user_id == user.id).all()


@router.delete("/apikey/{key_id}", status_code=204)
def delete_apikey(key_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    key = db.query(ApiKey).filter(ApiKey.id == key_id, ApiKey.user_id == user.id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API Key를 찾을 수 없습니다.")
    db.delete(key)
    db.commit()
