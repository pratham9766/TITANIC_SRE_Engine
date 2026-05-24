from __future__ import annotations

from app.config import settings
from app.services.telemetry import topology


class GraphService:
    async def upsert_topology(self) -> dict:
        try:
            from neo4j import AsyncGraphDatabase

            driver = AsyncGraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
            async with driver.session() as session:
                for node in topology():
                    await session.run(
                        """
                        MERGE (s:Service {id: $id})
                        SET s.name = $name, s.kind = $kind, s.health = $health, s.risk = $risk
                        """,
                        id=node.id,
                        name=node.name,
                        kind=node.kind,
                        health=node.health,
                        risk=node.risk,
                    )
                    for dep in node.depends_on:
                        await session.run(
                            """
                            MATCH (s:Service {id: $source})
                            MERGE (t:Service {id: $target})
                            MERGE (s)-[:DEPENDS_ON]->(t)
                            """,
                            source=node.id,
                            target=dep,
                        )
            await driver.close()
            return {"status": "ok", "services": len(topology())}
        except Exception as exc:
            return {"status": "demo", "error": str(exc), "services": len(topology())}

    async def blast_radius(self, service_id: str) -> dict:
        try:
            from neo4j import AsyncGraphDatabase

            driver = AsyncGraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH path = (s:Service {id: $service_id})<-[:DEPENDS_ON*0..4]-(dependent)
                    RETURN collect(distinct dependent.id) AS affected
                    """,
                    service_id=service_id,
                )
                record = await result.single()
            await driver.close()
            affected = record["affected"] if record else []
            if not affected:
                affected = self._fallback_blast_radius(service_id)
            return {"service": service_id, "affected": affected}
        except Exception:
            return {"service": service_id, "affected": self._fallback_blast_radius(service_id), "mode": "demo"}

    def _fallback_blast_radius(self, service_id: str) -> list[str]:
        fallback = {
            "db": ["database-rds", "payment-service", "checkout-service", "auth-service", "api-gateway"],
            "payment": ["payment-service", "checkout-service", "api-gateway"],
        }
        return fallback.get(service_id, [service_id])


graph_service = GraphService()
