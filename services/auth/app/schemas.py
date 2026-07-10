from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApiKeyCreate(BaseModel):
    key_name: Optional[str] = "기본키"
    api_type: Optional[str] = "weather"


class ApiKeyResponse(BaseModel):
    id: int
    key_name: str
    api_type: str
    key: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
