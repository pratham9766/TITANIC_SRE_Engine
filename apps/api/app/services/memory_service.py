from __future__ import annotations

import hashlib

from app.config import settings


class MemoryService:
    collection = "titanic_incident_memory"

    async def remember_incident(self, incident_id: str, summary: str) -> dict:
        point_id = int(hashlib.sha256(incident_id.encode()).hexdigest()[:12], 16)
        vector = self._demo_embedding(summary)
        try:
            from qdrant_client import AsyncQdrantClient
            from qdrant_client.models import Distance, PointStruct, VectorParams

            client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
            collections = await client.get_collections()
            names = {item.name for item in collections.collections}
            if self.collection not in names:
                await client.create_collection(self.collection, vectors_config=VectorParams(size=len(vector), distance=Distance.COSINE))
            await client.upsert(
                self.collection,
                points=[PointStruct(id=point_id, vector=vector, payload={"incident_id": incident_id, "summary": summary})],
            )
            await client.close()
            return {"status": "ok", "incident_id": incident_id}
        except Exception as exc:
            return {"status": "demo", "incident_id": incident_id, "error": str(exc)}

    async def similar_incidents(self, query: str) -> list[dict]:
        vector = self._demo_embedding(query)
        try:
            from qdrant_client import AsyncQdrantClient

            client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
            result = await client.search(self.collection, query_vector=vector, limit=5)
            await client.close()
            return [{"score": hit.score, **hit.payload} for hit in result]
        except Exception:
            return [
                {"incident_id": "INC-4712", "score": 0.91, "summary": "Prior DB connection pool exhaustion in payment-service."},
                {"incident_id": "INC-4688", "score": 0.84, "summary": "Retry amplification after deployment regression."},
            ]

    def _demo_embedding(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()
        return [byte / 255 for byte in digest[:32]]


memory_service = MemoryService()
