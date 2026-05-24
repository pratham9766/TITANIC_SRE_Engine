from fastapi import APIRouter

from app.services.telemetry import services
from app.services.telemetry_adapters import telemetry_hub

router = APIRouter(tags=["infrastructure"])


@router.get("/services")
def get_services():
    return services()


@router.get("/metrics")
async def get_metrics():
    return await telemetry_hub.current_metrics()
