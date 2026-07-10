from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    region_code = Column(String, index=True)
    region_name = Column(String)
    date = Column(Date, index=True)
    temp_max = Column(Float)
    temp_min = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    condition = Column(String)
