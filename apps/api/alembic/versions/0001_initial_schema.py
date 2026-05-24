"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-24
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("organizations", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(160), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("users", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("email", sa.String(320), nullable=False), sa.Column("name", sa.String(160), nullable=False), sa.Column("role", sa.String(32), server_default="viewer"), sa.Column("password_hash", sa.String(255)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.UniqueConstraint("email"))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("incidents", sa.Column("id", sa.String(32), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("title", sa.String(240), nullable=False), sa.Column("severity", sa.String(16)), sa.Column("status", sa.String(32)), sa.Column("root_cause", sa.Text()), sa.Column("confidence", sa.Integer()), sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("resolved_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_incidents_status", "incidents", ["status"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])
    op.create_table("deployments", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("service_name", sa.String(160)), sa.Column("version", sa.String(80)), sa.Column("commit_sha", sa.String(80)), sa.Column("deployed_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_deployments_service_name", "deployments", ["service_name"])
    op.create_index("ix_deployments_version", "deployments", ["version"])
    op.create_table("telemetry_events", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("incident_id", sa.String(32), sa.ForeignKey("incidents.id")), sa.Column("service_name", sa.String(160)), sa.Column("metric_name", sa.String(120)), sa.Column("metric_value", sa.Numeric()), sa.Column("unit", sa.String(32), server_default="count"), sa.Column("severity", sa.String(24)), sa.Column("observed_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_telemetry_service_metric_time", "telemetry_events", ["service_name", "metric_name", "observed_at"])
    op.create_table("ai_analysis", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("incident_id", sa.String(32), sa.ForeignKey("incidents.id")), sa.Column("agent_name", sa.String(80)), sa.Column("finding", sa.Text()), sa.Column("confidence", sa.Integer()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_ai_analysis_agent_name", "ai_analysis", ["agent_name"])
    op.create_table("recovery_actions", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("incident_id", sa.String(32), sa.ForeignKey("incidents.id")), sa.Column("action", sa.String(120)), sa.Column("risk", sa.String(32)), sa.Column("status", sa.String(32)), sa.Column("approved_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("command_preview", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_recovery_actions_status", "recovery_actions", ["status"])
    op.create_table("service_topology", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("source_service", sa.String(160)), sa.Column("target_service", sa.String(160)), sa.Column("relation", sa.String(64), server_default="depends_on"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_topology_source_target", "service_topology", ["source_service", "target_service"])
    op.create_table("memory_embeddings", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("source_type", sa.String(64)), sa.Column("source_id", sa.String(120)), sa.Column("summary", sa.Text()), sa.Column("embedding_ref", sa.String(240)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_memory_source", "memory_embeddings", ["source_type", "source_id"])
    op.create_table("audit_logs", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id")), sa.Column("actor_id", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("action", sa.String(120)), sa.Column("target_type", sa.String(80)), sa.Column("target_id", sa.String(160)), sa.Column("metadata_json", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_audit_actor_action", "audit_logs", ["actor_id", "action"])


def downgrade() -> None:
    for table in ["audit_logs", "memory_embeddings", "service_topology", "recovery_actions", "ai_analysis", "telemetry_events", "deployments", "incidents", "users", "organizations"]:
        op.drop_table(table)
