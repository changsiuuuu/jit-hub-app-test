from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import httpx

from ..database import get_db
from ..models import Tourist
from ..schemas import TouristListResponse, TouristResponse
from ..config import settings

router = APIRouter(tags=["tourist"])

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "32": "강원", "37": "경북", "39": "제주",
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


@router.get("/api/v3/tourist", response_model=TouristListResponse)
def get_tourists(
    api_key: str = Query(...),
    region: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key)

    query = db.query(Tourist)
    if region:
        if region not in REGION_MAP:
            raise HTTPException(status_code=400, detail="유효하지 않은 지역 코드입니다.")
        query = query.filter(Tourist.region_code == region)
    if category:
        query = query.filter(Tourist.category == category)

    items = query.order_by(Tourist.name).all()

    return TouristListResponse(
        region_code=region,
        region_name=REGION_MAP.get(region) if region else None,
        total=len(items),
        served_by=settings.jithub_location,
        items=items,
    )


@router.get("/api/v3/tourist/search/", response_model=TouristListResponse)
def search_tourist(
    api_key: str = Query(...),
    name: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key)

    items = (
        db.query(Tourist)
        .filter(Tourist.name.ilike(f"%{name}%"))
        .order_by(Tourist.name)
        .all()
    )

    return TouristListResponse(
        region_code=None,
        region_name=None,
        total=len(items),
        served_by=settings.jithub_location,
        items=items,
    )


@router.get("/api/v3/tourist/{tourist_id}", response_model=TouristResponse)
def get_tourist_detail(
    tourist_id: int,
    api_key: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key)

    tourist = db.query(Tourist).filter(Tourist.id == tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="관광지를 찾을 수 없습니다.")

    result = {c.name: getattr(tourist, c.name) for c in tourist.__table__.columns}
    result["served_by"] = settings.jithub_location
    return result
