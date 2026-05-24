from fastapi import APIRouter

from app.services.telemetry import replay

router = APIRouter(prefix="/replay", tags=["replay"])


@router.get("/{incident_id}")
def incident_replay(incident_id: str):
    return replay(incident_id)
