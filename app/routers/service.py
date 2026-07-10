from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..database import get_db
from ..models import ApiKey
from ..schemas import HealthResponse, TestServiceResponse
from ..config import settings

router = APIRouter(tags=["service"])


# ── /health ────────────────────────────────────────────────
@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        location=settings.jithub_location,
        timestamp=datetime.now(timezone.utc),
    )


# ── /api/v1/test-service ────────────────────────────────────
@router.get("/api/v1/test-service", response_model=TestServiceResponse)
def test_service(
    api_key: str = Query(..., description="발급된 API Key"),
    db: Session = Depends(get_db),
):
    key_record = db.query(ApiKey).filter(ApiKey.key == api_key).first()

    if not key_record:
        raise HTTPException(status_code=403, detail="유효하지 않은 API Key입니다.")

    if not key_record.is_active or key_record.status != "[활성]":
        raise HTTPException(status_code=403, detail="비활성화된 API Key입니다.")

    return TestServiceResponse(
        message="API 요청이 정상적으로 처리되었습니다.",
        served_by=settings.jithub_location,
        api_key=api_key,
        timestamp=datetime.now(timezone.utc),
    )
