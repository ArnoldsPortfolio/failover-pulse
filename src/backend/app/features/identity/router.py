from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db
from app.features.identity.service import IdentityService
router = APIRouter(prefix="/auth", tags=["auth"])
class Credentials(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
@router.post("/sign-up")
def sign_up(body: Credentials, db: Session = Depends(get_db)):
    return IdentityService(db).sign_up(body.email, body.password)
@router.post("/sign-in")
def sign_in(body: Credentials, db: Session = Depends(get_db)):
    return IdentityService(db).sign_in(body.email, body.password)
