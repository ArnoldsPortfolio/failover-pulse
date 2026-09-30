from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.probes.service import ProbeService
router = APIRouter(prefix="/targets", tags=["probes"])
class TargetBody(BaseModel):
    name: str
    kind: str = "ok"
    url: str = ""
    runbook: str = ""
class SampleBody(BaseModel):
    ok: bool
    detail: str = ""
class RunbookBody(BaseModel):
    text: str
@router.get("")
def list_targets(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ProbeService(db).list(user_id)
@router.post("")
def add_target(body: TargetBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ProbeService(db).add(user_id, body.name, body.kind, body.url, body.runbook)
@router.post("/tick")
def tick(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ProbeService(db).tick_all(user_id)
@router.post("/{target_id}/sample")
def sample(target_id: str, body: SampleBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ProbeService(db).record(user_id, target_id, body.ok, body.detail)
@router.post("/{target_id}/runbook")
def runbook(target_id: str, body: RunbookBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ProbeService(db).set_runbook(user_id, target_id, body.text)
