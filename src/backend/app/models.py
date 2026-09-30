from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base
from app.kernel.ids import new_id
class UserRow(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
class TargetRow(Base):
    __tablename__ = "targets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(80))
    kind: Mapped[str] = mapped_column(String(20), default="http")
    url: Mapped[str] = mapped_column(String(300), default="")
    state: Mapped[str] = mapped_column(String(16), default="healthy")
    streak_fail: Mapped[int] = mapped_column(Integer, default=0)
    streak_ok: Mapped[int] = mapped_column(Integer, default=0)
    draining: Mapped[int] = mapped_column(Integer, default=0)
    runbook: Mapped[str] = mapped_column(Text, default="")
class SampleRow(Base):
    __tablename__ = "samples"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    target_id: Mapped[str] = mapped_column(String(36), index=True)
    ok: Mapped[int] = mapped_column(Integer)
    detail: Mapped[str] = mapped_column(String(200), default="")
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class AlertRow(Base):
    __tablename__ = "alerts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    target_id: Mapped[str] = mapped_column(String(36), index=True)
    message: Mapped[str] = mapped_column(String(200))
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
