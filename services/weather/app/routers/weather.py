from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
import httpx

from ..database import get_db
from ..models import Weather
from ..schemas import WeatherListResponse
from ..config import settings

router = APIRouter(tags=["weather"])

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "39": "제주",
}


def verify_api_key(api_key: str):
    try:
        res = httpx.get(
            f"{settings.auth_service_url}/internal/verify",
            params={"api_key": api_key},
            timeout=5.0,
        )
        data = res.json()
    except Exception:
        raise HTTPException(status_code=503, detail="인증 서비스에 연결할 수 없습니다.")
    if not data.get("valid"):
        raise HTTPException(status_code=403, detail="유효하지 않은 API Key입니다.")


@router.get("/api/v1/weather", response_model=WeatherListResponse)
def get_weather(
    api_key: str = Query(...),
    region: str = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key)

    if region not in REGION_MAP:
        raise HTTPException(status_code=400, detail="유효하지 않은 지역 코드입니다.")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="시작일이 종료일보다 클 수 없습니다.")

    items = (
        db.query(Weather)
        .filter(
            Weather.region_code == region,
            Weather.date >= start_date,
            Weather.date <= end_date,
        )
        .order_by(Weather.date)
        .all()
    )

    return WeatherListResponse(
        region_code=region,
        region_name=REGION_MAP[region],
        start_date=start_date,
        end_date=end_date,
        total=len(items),
        served_by=settings.jithub_location,
        items=items,
    )


@router.get("/api/v1/weather/regions")
def get_regions():
    return {"regions": [{"code": k, "name": v} for k, v in REGION_MAP.items()]}
