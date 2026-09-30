from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import TargetRow
class StatusService:
    def __init__(self, db: Session):
        self.db = db
    def snapshot(self) -> dict:
        rows = list(self.db.scalars(select(TargetRow)))
        services = [{"name": t.name, "state": t.state, "runbook": t.runbook, "draining": bool(t.draining)} for t in rows]
        worst = "operational"
        if any(s["state"] == "down" for s in services):
            worst = "outage"
        elif any(s["state"] in {"degraded", "draining"} for s in services):
            worst = "degraded"
        return {"status": worst, "services": services}
