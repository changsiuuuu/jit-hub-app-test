from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


# ── Auth ───────────────────────────────────────────────────
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


# ── API Key ────────────────────────────────────────────────
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


# ── Weather ────────────────────────────────────────────────
class WeatherResponse(BaseModel):
    id: int
    region_code: str
    region_name: str
    date: date
    temp_max: Optional[float]
    temp_min: Optional[float]
    humidity: Optional[float]
    precipitation: Optional[float]
    condition: Optional[str]

    class Config:
        from_attributes = True


class WeatherListResponse(BaseModel):
    region_code: str
    region_name: str
    start_date: date
    end_date: date
    total: int
    served_by: str
    items: list[WeatherResponse]


# ── Traffic ────────────────────────────────────────────────
class TrafficRouteResponse(BaseModel):
    id: int
    region_code: str
    region_name: str
    type: str
    route_name: str
    start_stop: Optional[str]
    end_stop: Optional[str]
    congestion: Optional[str]
    interval_min: Optional[int]

    class Config:
        from_attributes = True


class TrafficListResponse(BaseModel):
    region_code: str
    region_name: str
    type: str
    total: int
    served_by: str
    items: list[TrafficRouteResponse]


# ── Tourist ────────────────────────────────────────────────
class TouristResponse(BaseModel):
    id: int
    name: str
    region_code: str
    region_name: str
    category: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    admission_fee: Optional[int]
    admission_info: Optional[str]
    peak_season: Optional[str]
    off_season: Optional[str]
    open_hours: Optional[str]
    image_url: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class TouristListResponse(BaseModel):
    region_code: Optional[str]
    region_name: Optional[str]
    total: int
    served_by: str
    items: list[TouristResponse]


# ── Service ────────────────────────────────────────────────
class HealthResponse(BaseModel):
    status: str
    location: str
    timestamp: datetime


class TestServiceResponse(BaseModel):
    message: str
    served_by: str
    api_key: str
    timestamp: datetime
