from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ApiKey, TrafficRoute
from ..schemas import TrafficListResponse
from ..config import settings

router = APIRouter(tags=["traffic"])

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "26": "울산", "39": "제주",
}


# ── 교통 노선 조회 ──────────────────────────────────────────
@router.get("/api/v2/traffic", response_model=TrafficListResponse)
def get_traffic(
    api_key: str = Query(..., description="발급된 API Key"),
    region: str = Query(..., description="지역 코드 (예: 11=서울, 21=부산)"),
    type: str = Query("bus", description="교통 유형: bus / subway"),
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
        raise HTTPException(status_code=400, detail=f"유효하지 않은 지역 코드입니다.")

    # 교통 유형 검증
    if type not in ["bus", "subway"]:
        raise HTTPException(status_code=400, detail="type은 bus 또는 subway만 가능합니다.")

    items = (
        db.query(TrafficRoute)
        .filter(TrafficRoute.region_code == region, TrafficRoute.type == type)
        .order_by(TrafficRoute.route_name)
        .all()
    )

    return TrafficListResponse(
        region_code=region,
        region_name=REGION_MAP[region],
        type=type,
        total=len(items),
        served_by=settings.jithub_location,
        items=items,
    )
