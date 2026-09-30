from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.ids import new_id
from app.models import AlertRow, TargetRow
class AlertService:
    def __init__(self, db: Session):
        self.db = db
    def emit_change(self, target: TargetRow, previous: str) -> None:
        if previous == target.state:
            return
        last = self.db.scalars(select(AlertRow).where(AlertRow.target_id == target.id).order_by(AlertRow.at.desc())).first()
        msg = f"{target.name}: {previous} → {target.state}"
        if last and last.message == msg:
            return
        self.db.add(AlertRow(id=new_id(), owner_id=target.owner_id, target_id=target.id, message=msg))
    def list(self, owner_id: str) -> list[dict]:
        rows = self.db.scalars(select(AlertRow).where(AlertRow.owner_id == owner_id).order_by(AlertRow.at.desc()).limit(50))
        return [{"id": r.id, "target_id": r.target_id, "message": r.message, "at": r.at.isoformat()} for r in rows]
