from fastapi import APIRouter, HTTPException

from app.schemas import LoginRequest
from app.services.auth_service import login

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def auth_login(request: LoginRequest):
    try:
        return login(request)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
