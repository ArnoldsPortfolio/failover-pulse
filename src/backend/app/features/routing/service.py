from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.errors import Conflict, NotFound
from app.models import TargetRow
class RouteService:
    def __init__(self, db: Session):
        self.db = db
    def choose(self, owner_id: str) -> dict:
        rows = list(self.db.scalars(select(TargetRow).where(TargetRow.owner_id == owner_id, TargetRow.draining == 0, TargetRow.state == "healthy")))
        if not rows:
            raise Conflict("No healthy target")
        t = rows[0]
        return {"id": t.id, "name": t.name, "url": t.url, "state": t.state}
    def drain(self, owner_id: str, target_id: str) -> dict:
        t = self.db.get(TargetRow, target_id)
        if not t or t.owner_id != owner_id:
            raise NotFound("Target not found")
        t.draining = 1; t.state = "draining"; self.db.commit()
        return {"id": t.id, "state": t.state, "draining": True}
    def undrain(self, owner_id: str, target_id: str) -> dict:
        t = self.db.get(TargetRow, target_id)
        if not t or t.owner_id != owner_id:
            raise NotFound("Target not found")
        t.draining = 0; t.state = "healthy"; t.streak_fail = 0; self.db.commit()
        return {"id": t.id, "state": t.state, "draining": False}
