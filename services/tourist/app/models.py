from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Tourist(Base):
    __tablename__ = "tourists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_code = Column(String, index=True)
    region_name = Column(String)
    category = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    admission_fee = Column(Integer, default=0)
    admission_info = Column(String)
    peak_season = Column(String)
    off_season = Column(String)
    open_hours = Column(String)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
