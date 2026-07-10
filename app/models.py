from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete")


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key_name = Column(String(100), nullable=False, default="기본키")
    api_type = Column(String(50), nullable=False, default="weather")  # weather, traffic, food 등
    key = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="[활성]")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="api_keys")


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    region_code = Column(String(10), nullable=False, index=True)
    region_name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False, index=True)
    temp_max = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    condition = Column(String(50), nullable=True)


class TrafficRoute(Base):
    __tablename__ = "traffic_routes"

    id = Column(Integer, primary_key=True, index=True)
    region_code = Column(String(10), nullable=False, index=True)
    region_name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)        # bus / subway
    route_name = Column(String(100), nullable=False) # 예: 1호선, 101번
    start_stop = Column(String(100), nullable=True)  # 출발지
    end_stop = Column(String(100), nullable=True)    # 종착지
    congestion = Column(String(20), nullable=True)   # 낮음 / 보통 / 높음
    interval_min = Column(Integer, nullable=True)    # 배차 간격(분)


class Tourist(Base):
    __tablename__ = "tourists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    region_code = Column(String(10), nullable=False, index=True)
    region_name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=True)       # 자연, 문화, 역사, 테마파크 등
    address = Column(String(200), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    admission_fee = Column(Integer, nullable=True)     # 입장료(원), 0이면 무료
    admission_info = Column(String(200), nullable=True)# 성인/청소년/어린이 등 상세
    peak_season = Column(String(100), nullable=True)   # 성수기 (예: 7월~8월)
    off_season = Column(String(100), nullable=True)    # 비성수기 (예: 11월~2월)
    open_hours = Column(String(100), nullable=True)    # 운영시간
    image_url = Column(String(500), nullable=True)     # 이미지 URL (S3 or static)
    description = Column(String(1000), nullable=True)
