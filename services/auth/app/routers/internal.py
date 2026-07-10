from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ApiKey

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/verify")
def verify_api_key(api_key: str = Query(...), db: Session = Depends(get_db)):
    key_record = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    if not key_record:
        return {"valid": False, "reason": "Key not found"}
    if not key_record.is_active or key_record.status != "[활성]":
        return {"valid": False, "reason": "Key inactive"}
    return {"valid": True, "api_type": key_record.api_type}
