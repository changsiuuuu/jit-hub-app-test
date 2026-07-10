from sqlalchemy import Column, Integer, String
from .database import Base


class TrafficRoute(Base):
    __tablename__ = "traffic_routes"
    id = Column(Integer, primary_key=True, index=True)
    region_code = Column(String, index=True)
    region_name = Column(String)
    type = Column(String)
    route_name = Column(String)
    start_stop = Column(String)
    end_stop = Column(String)
    congestion = Column(String)
    interval_min = Column(Integer)
