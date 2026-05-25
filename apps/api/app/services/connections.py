from __future__ import annotations

import asyncio
import socket
from typing import Any

import httpx

from app.config import settings
from app.db import check_database


async def check_redis() -> dict[str, Any]:
    try:
        from redis.asyncio import Redis

        client = Redis.from_url(settings.redis_url, socket_connect_timeout=1)
        await asyncio.wait_for(client.ping(), timeout=1.5)
        try:
            await client.aclose()
        except Exception:
            pass
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


async def check_neo4j() -> dict[str, Any]:
    return await asyncio.to_thread(_check_socket, "127.0.0.1", 7687, "bolt")


async def check_qdrant() -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{settings.qdrant_url.rstrip('/')}/collections")
            response.raise_for_status()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


def _check_socket(host: str, port: int, protocol: str) -> dict[str, Any]:
    try:
        with socket.create_connection((host, port), timeout=1.5):
            return {"status": "ok", "protocol": protocol}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc), "protocol": protocol}


async def check_openai() -> dict[str, Any]:
    if not settings.openai_api_key:
        return {"status": "demo", "error": "OPENAI_API_KEY not configured"}
    return {"status": "configured", "model": settings.openai_model}


async def system_health() -> dict[str, Any]:
    async def guarded(name: str, check, timeout: float = 3) -> dict[str, Any]:
        try:
            if name == "database":
                return await asyncio.wait_for(asyncio.to_thread(check), timeout=timeout)
            return await asyncio.wait_for(check(), timeout=timeout)
        except Exception as exc:
            return {"status": "degraded", "error": str(exc) or "health check timed out"}

    database, redis, neo4j, qdrant, openai = await asyncio.gather(
        guarded("database", check_database),
        guarded("redis", check_redis),
        guarded("neo4j", check_neo4j),
        guarded("qdrant", check_qdrant),
        guarded("openai", check_openai, timeout=1),
    )
    return {
        "api": "ok",
        "database": database,
        "redis": redis,
        "neo4j": neo4j,
        "qdrant": qdrant,
        "openai": openai,
    }
