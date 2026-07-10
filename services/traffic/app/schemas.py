from pydantic import BaseModel
from typing import List


class TrafficRouteItem(BaseModel):
    id: int
    region_code: str
    region_name: str
    type: str
    route_name: str
    start_stop: str
    end_stop: str
    congestion: str
    interval_min: int

    class Config:
        from_attributes = True


class TrafficListResponse(BaseModel):
    region_code: str
    region_name: str
    type: str
    total: int
    served_by: str
    items: List[TrafficRouteItem]
