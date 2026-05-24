from fastapi import APIRouter

from app.services.memory_service import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("/similar")
async def similar(q: str):
    return await memory_service.similar_incidents(q)


@router.post("/remember/{incident_id}")
async def remember(incident_id: str, summary: str):
    return await memory_service.remember_incident(incident_id, summary)
