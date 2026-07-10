from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import httpx

from ..database import get_db
from ..models import TrafficRoute
from ..schemas import TrafficListResponse
from ..config import settings

router = APIRouter(tags=["traffic"])

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


@router.get("/api/v2/traffic", response_model=TrafficListResponse)
def get_traffic(
    api_key: str = Query(...),
    region: str = Query(...),
    type: str = Query("bus"),
    db: Session = Depends(get_db),
):
    verify_api_key(api_key)

    if region not in REGION_MAP:
        raise HTTPException(status_code=400, detail="유효하지 않은 지역 코드입니다.")
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
