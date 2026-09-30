import hashlib
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.errors import Unauthorized
from app.kernel.ids import new_id
from app.kernel.tokens import issue_access
from app.models import UserRow
from app.settings import Settings
class IdentityService:
    def __init__(self, db: Session):
        self.db = db
    def sign_up(self, email: str, password: str) -> dict:
        if self.db.scalar(select(UserRow).where(UserRow.email == email.lower())):
            raise Unauthorized("Email already used")
        user = UserRow(id=new_id(), email=email.lower(), password_hash=_hash(password))
        self.db.add(user); self.db.commit()
        return self.issue(user)
    def sign_in(self, email: str, password: str) -> dict:
        user = self.db.scalar(select(UserRow).where(UserRow.email == email.lower()))
        if not user or user.password_hash != _hash(password):
            raise Unauthorized("Bad credentials")
        return self.issue(user)
    def issue(self, user: UserRow) -> dict:
        return {"access_token": issue_access(Settings().app_secret, user.id), "email": user.email}
def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
