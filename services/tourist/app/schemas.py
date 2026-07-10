from pydantic import BaseModel
from typing import Optional, List


class TouristItem(BaseModel):
    id: int
    name: str
    region_code: str
    region_name: str
    category: str
    address: str
    latitude: float
    longitude: float
    admission_fee: int
    admission_info: str
    peak_season: str
    off_season: str
    open_hours: str
    image_url: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TouristListResponse(BaseModel):
    region_code: Optional[str] = None
    region_name: Optional[str] = None
    total: int
    served_by: str
    items: List[TouristItem]


class TouristResponse(TouristItem):
    served_by: str
