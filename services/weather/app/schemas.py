from pydantic import BaseModel
from datetime import date
from typing import List


class WeatherItem(BaseModel):
    id: int
    region_code: str
    region_name: str
    date: date
    temp_max: float
    temp_min: float
    humidity: float
    precipitation: float
    condition: str

    class Config:
        from_attributes = True


class WeatherListResponse(BaseModel):
    region_code: str
    region_name: str
    start_date: date
    end_date: date
    total: int
    served_by: str
    items: List[WeatherItem]
