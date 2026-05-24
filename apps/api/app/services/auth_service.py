from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings
from app.schemas import LoginRequest, TokenResponse


DEMO_USERS = {
    "admin@titanic.local": {"password": "titanic-demo", "role": "sre_admin", "name": "Demo Admin"},
    "viewer@titanic.local": {"password": "titanic-demo", "role": "viewer", "name": "Demo Viewer"},
}


def login(request: LoginRequest) -> TokenResponse:
    user = DEMO_USERS.get(request.email)
    if not user or user["password"] != request.password:
        raise ValueError("Invalid email or password")
    now = datetime.now(timezone.utc)
    payload = {
        "sub": request.email,
        "role": user["role"],
        "iss": settings.jwt_issuer,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=8)).timestamp()),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return TokenResponse(access_token=token, role=user["role"])


def verify_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)
