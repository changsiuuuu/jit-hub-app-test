from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import ApiKey, Tourist
from ..schemas import TouristListResponse, TouristResponse
from ..config import settings

router = APIRouter(tags=["tourist"])

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "32": "강원", "37": "경북", "39": "제주",
}


def verify_api_key(api_key: str, db: Session):
    key_record = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    if not key_record:
        raise HTTPException(status_code=403, detail="유효하지 않은 API Key입니다.")
    if not key_record.is_active or key_record.status != "[활성]":
        raise HTTPException(status_code=403, detail="비활성화된 API Key입니다.")


# ── 관광지 목록 조회 (지역별) ───────────────────────────────
@router.get("/api/v3/tourist", response_model=TouristListResponse)
def get_tourists(
    api_key: str = Query(..., description="발급된 API Key"),
    region: Optional[str] = Query(None, description="지역 코드 (미입력 시 전체)"),
    category: Optional[str] = Query(None, description="카테고리: 자연, 문화, 역사, 테마파크"),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key, db)

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


# ── 관광지 상세 조회 ────────────────────────────────────────
@router.get("/api/v3/tourist/{tourist_id}", response_model=TouristResponse)
def get_tourist_detail(
    tourist_id: int,
    api_key: str = Query(..., description="발급된 API Key"),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key, db)

    tourist = db.query(Tourist).filter(Tourist.id == tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="관광지를 찾을 수 없습니다.")
    return tourist


# ── 관광지 이름 검색 ────────────────────────────────────────
@router.get("/api/v3/tourist/search/", response_model=TouristListResponse)
def search_tourist(
    api_key: str = Query(..., description="발급된 API Key"),
    name: str = Query(..., description="관광지 이름 검색어"),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key, db)

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
