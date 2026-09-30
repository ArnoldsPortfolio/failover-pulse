from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.routing.service import RouteService
router = APIRouter(tags=["routing"])
@router.get("/route")
def choose(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return RouteService(db).choose(user_id)
@router.post("/targets/{target_id}/drain")
def drain(target_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return RouteService(db).drain(user_id, target_id)
@router.post("/targets/{target_id}/undrain")
def undrain(target_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return RouteService(db).undrain(user_id, target_id)
