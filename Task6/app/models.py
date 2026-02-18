from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    DateTime, JSON, UniqueConstraint, Index
)
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    event_id = Column(String)
    event_type = Column(String, index=True)
    event_timestamp = Column(DateTime(timezone=True), index=True)
    processed_at = Column(DateTime(timezone=True))
    payload = Column(JSON)
    status = Column(String)
    processing_latency_ms = Column(Integer)

    __table_args__ = (
        UniqueConstraint("client_id", "event_id", name="uq_client_event"),
        Index("idx_client_type", "client_id", "event_type"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
