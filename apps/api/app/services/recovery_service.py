from __future__ import annotations

import uuid

from app.config import settings
from app.schemas import RecoveryExecution, RecoveryPlan, RecoveryRequest


class RecoveryService:
    def plan(self, action: str) -> RecoveryPlan:
        previews = {
            "scale-rds": "aws rds modify-db-instance --db-instance-class db.r7g.large",
            "restart-payment": "kubectl rollout restart deployment/payment-service",
            "rollback": "argocd app rollback payment-service v2.1.3",
            "scale-replicas": "kubectl scale deployment checkout-service --replicas=8",
        }
        return RecoveryPlan(
            action=action,
            risk="medium" if action not in {"scale-rds", "scale-replicas"} else "low",
            requires_approval=settings.require_human_approval,
            command_preview=previews.get(action, "manual runbook action"),
            rollback_plan="Verify SLOs and revert capacity or deployment change if health regresses.",
            dry_run=settings.recovery_dry_run or not settings.allow_production_writes,
            status="planned",
        )

    def execute(self, request: RecoveryRequest) -> RecoveryExecution:
        plan = self.plan(request.action)
        if settings.require_human_approval and not request.approved_by:
            return RecoveryExecution(
                incident_id=request.incident_id,
                action=request.action,
                status="blocked",
                dry_run=True,
                audit_id=str(uuid.uuid4()),
                output="Human approval is required before execution.",
            )
        if plan.dry_run:
            return RecoveryExecution(
                incident_id=request.incident_id,
                action=request.action,
                status="dry_run_complete",
                dry_run=True,
                audit_id=str(uuid.uuid4()),
                output=f"Dry run accepted. Would execute: {plan.command_preview}",
            )
        return RecoveryExecution(
            incident_id=request.incident_id,
            action=request.action,
            status="queued",
            dry_run=False,
            audit_id=str(uuid.uuid4()),
            output="Execution queued behind policy and audit controls.",
        )


recovery_service = RecoveryService()
