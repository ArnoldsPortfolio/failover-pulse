from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.alerts.service import AlertService
router = APIRouter(prefix="/alerts", tags=["alerts"])
@router.get("")
def list_alerts(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return AlertService(db).list(user_id)
