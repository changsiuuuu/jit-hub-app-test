from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import uuid

from ..database import get_db
from ..models import User, ApiKey
from ..schemas import SignupRequest, LoginRequest, TokenResponse, UserResponse, ApiKeyCreate, ApiKeyResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = "jithub-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="인증 토큰이 유효하지 않습니다.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user


# ── 회원가입 ────────────────────────────────────────────────
@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    user = User(
        email=payload.email,
        password=pwd_context.hash(payload.password),
        name=payload.name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── 로그인 ─────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    return TokenResponse(access_token=create_access_token(user.id))


# ── 내 정보 조회 ────────────────────────────────────────────
@router.get("/me", response_model=UserResponse)
def get_me(token: str, db: Session = Depends(get_db)):
    return get_current_user(token, db)


# ── API Key 발급 ────────────────────────────────────────────
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


# ── API Key 목록 조회 ───────────────────────────────────────
@router.get("/apikey", response_model=list[ApiKeyResponse])
def get_apikeys(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return db.query(ApiKey).filter(ApiKey.user_id == user.id).all()


# ── API Key 비활성화 ────────────────────────────────────────
@router.delete("/apikey/{key_id}", status_code=204)
def delete_apikey(key_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    key = db.query(ApiKey).filter(ApiKey.id == key_id, ApiKey.user_id == user.id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API Key를 찾을 수 없습니다.")
    key.is_active = False
    key.status = "[비활성]"
    db.commit()
