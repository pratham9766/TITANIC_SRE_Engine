from fastapi import APIRouter

from app.schemas import RecoveryRequest
from app.services.ai_engine import recovery_plan
from app.services.recovery_service import recovery_service

router = APIRouter(prefix="/recovery", tags=["recovery"])


@router.post("/plan")
def plan(request: RecoveryRequest):
    return recovery_plan(request.action)


@router.post("/execute")
def execute(request: RecoveryRequest):
    return recovery_service.execute(request)
