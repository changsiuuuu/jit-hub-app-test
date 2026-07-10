from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from ..database import get_db
from ..models import ApiKey, Weather
from ..schemas import WeatherListResponse
from ..config import settings

router = APIRouter(tags=["weather"])

# 지역 코드 목록
REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "26": "울산", "29": "세종", "31": "경기",
    "32": "강원", "33": "충북", "34": "충남",
    "35": "전북", "36": "전남", "37": "경북",
    "38": "경남", "39": "제주",
}


# ── 날씨 정보 조회 ──────────────────────────────────────────
@router.get("/api/v1/weather", response_model=WeatherListResponse)
def get_weather(
    api_key: str = Query(..., description="발급된 API Key"),
    region: str = Query(..., description="지역 코드 (예: 11=서울, 21=부산)"),
    start_date: date = Query(..., description="조회 시작일 (YYYY-MM-DD)"),
    end_date: date = Query(..., description="조회 종료일 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    # API Key 검증
    key_record = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    if not key_record:
        raise HTTPException(status_code=403, detail="유효하지 않은 API Key입니다.")
    if not key_record.is_active or key_record.status != "[활성]":
        raise HTTPException(status_code=403, detail="비활성화된 API Key입니다.")

    # 지역 코드 검증
    if region not in REGION_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"유효하지 않은 지역 코드입니다. 사용 가능: {list(REGION_MAP.keys())}"
        )

    # 날짜 범위 검증
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="시작일이 종료일보다 클 수 없습니다.")

    # 날씨 데이터 조회
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


# ── 지역 코드 목록 조회 ─────────────────────────────────────
@router.get("/api/v1/weather/regions")
def get_regions():
    return [{"code": k, "name": v} for k, v in REGION_MAP.items()]
