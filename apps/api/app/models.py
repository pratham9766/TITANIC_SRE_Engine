import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(160), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="organization")
    incidents: Mapped[list["IncidentRecord"]] = relationship(back_populates="organization")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    role: Mapped[str] = mapped_column(String(32), default="viewer")
    password_hash: Mapped[str | None] = mapped_column(String(255))

    organization: Mapped[Organization] = relationship(back_populates="users")
    approvals: Mapped[list["RecoveryAction"]] = relationship(back_populates="approver")


class IncidentRecord(Base, TimestampMixin):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    root_cause: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization: Mapped[Organization | None] = relationship(back_populates="incidents")
    telemetry_events: Mapped[list["TelemetryEvent"]] = relationship(back_populates="incident")
    ai_analysis: Mapped[list["AIAnalysis"]] = relationship(back_populates="incident")
    recovery_actions: Mapped[list["RecoveryAction"]] = relationship(back_populates="incident")


class TelemetryEvent(Base, TimestampMixin):
    __tablename__ = "telemetry_events"
    __table_args__ = (Index("ix_telemetry_service_metric_time", "service_name", "metric_name", "observed_at"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str | None] = mapped_column(ForeignKey("incidents.id"), index=True)
    service_name: Mapped[str] = mapped_column(String(160), index=True)
    metric_name: Mapped[str] = mapped_column(String(120), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric)
    unit: Mapped[str] = mapped_column(String(32), default="count")
    severity: Mapped[str] = mapped_column(String(24), index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    incident: Mapped[IncidentRecord | None] = relationship(back_populates="telemetry_events")


class Deployment(Base, TimestampMixin):
    __tablename__ = "deployments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    service_name: Mapped[str] = mapped_column(String(160), index=True)
    version: Mapped[str] = mapped_column(String(80), index=True)
    commit_sha: Mapped[str | None] = mapped_column(String(80))
    deployed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class AIAnalysis(Base, TimestampMixin):
    __tablename__ = "ai_analysis"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    agent_name: Mapped[str] = mapped_column(String(80), index=True)
    finding: Mapped[str] = mapped_column(Text)
    confidence: Mapped[int] = mapped_column(Integer)

    incident: Mapped[IncidentRecord] = relationship(back_populates="ai_analysis")


class RecoveryAction(Base, TimestampMixin):
    __tablename__ = "recovery_actions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    action: Mapped[str] = mapped_column(String(120))
    risk: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), index=True)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    command_preview: Mapped[str | None] = mapped_column(Text)

    incident: Mapped[IncidentRecord] = relationship(back_populates="recovery_actions")
    approver: Mapped[User | None] = relationship(back_populates="approvals")


class ServiceTopology(Base, TimestampMixin):
    __tablename__ = "service_topology"
    __table_args__ = (Index("ix_topology_source_target", "source_service", "target_service"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    source_service: Mapped[str] = mapped_column(String(160))
    target_service: Mapped[str] = mapped_column(String(160))
    relation: Mapped[str] = mapped_column(String(64), default="depends_on")


class MemoryEmbedding(Base, TimestampMixin):
    __tablename__ = "memory_embeddings"
    __table_args__ = (Index("ix_memory_source", "source_type", "source_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    source_type: Mapped[str] = mapped_column(String(64))
    source_id: Mapped[str] = mapped_column(String(120))
    summary: Mapped[str] = mapped_column(Text)
    embedding_ref: Mapped[str] = mapped_column(String(240))


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_actor_action", "actor_id", "action"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    target_type: Mapped[str] = mapped_column(String(80))
    target_id: Mapped[str] = mapped_column(String(160))
    metadata_json: Mapped[str | None] = mapped_column(Text)
