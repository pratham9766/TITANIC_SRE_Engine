from fastapi import APIRouter

from app.services.telemetry import metrics, services, topology
from app.services.graph_service import graph_service

router = APIRouter(prefix="/topology", tags=["topology"])


@router.get("")
def get_topology():
    return topology()


@router.get("/services")
def get_services():
    return services()


@router.get("/metrics")
def get_metrics():
    return metrics()


@router.post("/sync")
async def sync_topology():
    return await graph_service.upsert_topology()


@router.get("/blast-radius/{service_id}")
async def blast_radius(service_id: str):
    return await graph_service.blast_radius(service_id)
