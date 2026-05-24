from __future__ import annotations

import asyncio
from typing import Any

from app.config import settings
from app.db import check_database


async def check_redis() -> dict[str, Any]:
    try:
        from redis.asyncio import Redis

        client = Redis.from_url(settings.redis_url, socket_connect_timeout=1)
        await asyncio.wait_for(client.ping(), timeout=1.5)
        await client.aclose()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


async def check_neo4j() -> dict[str, Any]:
    try:
        from neo4j import AsyncGraphDatabase

        driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
            connection_timeout=1,
        )
        async with driver.session() as session:
            await asyncio.wait_for(session.run("RETURN 1"), timeout=1.5)
        await driver.close()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


async def check_qdrant() -> dict[str, Any]:
    try:
        from qdrant_client import AsyncQdrantClient

        client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        await asyncio.wait_for(client.get_collections(), timeout=1.5)
        await client.close()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


async def check_openai() -> dict[str, Any]:
    if not settings.openai_api_key:
        return {"status": "demo", "error": "OPENAI_API_KEY not configured"}
    return {"status": "configured", "model": settings.openai_model}


async def system_health() -> dict[str, Any]:
    database, redis, neo4j, qdrant, openai = await asyncio.gather(
        asyncio.to_thread(check_database),
        check_redis(),
        check_neo4j(),
        check_qdrant(),
        check_openai(),
    )
    return {
        "api": "ok",
        "database": database,
        "redis": redis,
        "neo4j": neo4j,
        "qdrant": qdrant,
        "openai": openai,
    }
