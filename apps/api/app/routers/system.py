from fastapi import APIRouter

from app.services.connections import system_health

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
async def health():
    return await system_health()
