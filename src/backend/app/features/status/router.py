from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.features.status.service import StatusService
router = APIRouter(tags=["status"])
@router.get("/status")
def public_status(db: Session = Depends(get_db)):
    return StatusService(db).snapshot()
