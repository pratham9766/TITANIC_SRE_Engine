from fastapi import APIRouter

from app.services.telemetry import active_incidents, get_incident, incident_timeline

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("")
def list_incidents():
    return active_incidents()


@router.get("/{incident_id}")
def incident_detail(incident_id: str):
    return get_incident(incident_id)


@router.get("/{incident_id}/timeline")
def get_timeline(incident_id: str):
    return incident_timeline(incident_id)
