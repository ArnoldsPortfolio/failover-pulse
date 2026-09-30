from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.alerts.service import AlertService
from app.kernel.errors import NotFound
from app.kernel.ids import new_id
from app.models import SampleRow, TargetRow
from app.settings import Settings
class ProbeService:
    def __init__(self, db: Session):
        self.db = db
    def add(self, owner_id: str, name: str, kind: str, url: str, runbook: str = "") -> dict:
        row = TargetRow(id=new_id(), owner_id=owner_id, name=name[:80], kind=kind, url=url[:300], runbook=runbook)
        self.db.add(row); self.db.commit()
        return _out(row)
    def list(self, owner_id: str) -> list[dict]:
        return [_out(t) for t in self.db.scalars(select(TargetRow).where(TargetRow.owner_id == owner_id))]
    def get(self, owner_id: str, target_id: str) -> TargetRow:
        row = self.db.get(TargetRow, target_id)
        if not row or row.owner_id != owner_id:
            raise NotFound("Target not found")
        return row
    def record(self, owner_id: str, target_id: str, ok: bool, detail: str = "") -> dict:
        target = self.get(owner_id, target_id)
        previous = target.state
        self.db.add(SampleRow(id=new_id(), target_id=target.id, ok=int(ok), detail=detail[:200]))
        if ok:
            target.streak_ok += 1; target.streak_fail = 0
            if target.state != "draining" and target.streak_ok >= Settings().recover_threshold:
                target.state = "healthy"
        else:
            target.streak_fail += 1; target.streak_ok = 0
            if target.streak_fail >= Settings().fail_threshold:
                target.state = "down"
            elif target.state == "healthy":
                target.state = "degraded"
        if target.draining:
            target.state = "draining"
        AlertService(self.db).emit_change(target, previous)
        self.db.commit()
        return _out(target)
    def tick_all(self, owner_id: str) -> list[dict]:
        ids = [t.id for t in self.db.scalars(select(TargetRow).where(TargetRow.owner_id == owner_id))]
        out = []
        for target_id in ids:
            target = self.get(owner_id, target_id)
            ok, detail = _probe(target)
            out.append(self.record(owner_id, target_id, ok, detail))
        return out
    def set_runbook(self, owner_id: str, target_id: str, text: str) -> dict:
        target = self.get(owner_id, target_id)
        target.runbook = text[:2000]
        self.db.commit()
        return _out(target)
def _probe(target: TargetRow) -> tuple[bool, str]:
    if target.kind == "fail":
        return False, "forced fail"
    if target.kind == "ok":
        return True, "forced ok"
    if target.url.startswith("down://"):
        return False, "simulated down"
    return True, "ok"
def _out(t: TargetRow) -> dict:
    return {"id": t.id, "name": t.name, "kind": t.kind, "url": t.url, "state": t.state, "streak_fail": t.streak_fail, "streak_ok": t.streak_ok, "draining": bool(t.draining), "runbook": t.runbook}
