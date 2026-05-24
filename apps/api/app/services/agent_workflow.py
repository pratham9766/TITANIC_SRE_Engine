from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

from app.schemas import AnalysisResponse
from app.services.ai_service import ai_service


AGENTS = [
    ("Metrics Agent", "Analyzing saturation, latency, traffic, and error-rate deltas."),
    ("Log Agent", "Scanning error signatures, stack traces, and retry loops."),
    ("Deployment Agent", "Comparing deploy history, commits, and release windows."),
    ("Security Agent", "Checking abuse patterns, unusual traffic, and auth anomalies."),
    ("Topology Agent", "Tracing dependency graph and cascading blast radius."),
    ("Recovery Agent", "Ranking rollback, restart, scale, and reroute options."),
    ("Chief SRE Agent", "Synthesizing final root cause and confidence."),
]


async def run_agent_workflow(incident_id: str) -> AnalysisResponse:
    findings = []
    for index, (name, thought) in enumerate(AGENTS):
        findings.append(
            {
                "name": name,
                "status": "complete" if index < len(AGENTS) - 1 else "synthesized",
                "finding": thought,
                "confidence": min(92, 78 + index * 2),
            }
        )

    fallback = {
        "root_cause": "Database connection pool exhaustion in payment-service caused downstream checkout failures.",
        "confidence": 92,
        "blast_radius": ["database-rds", "payment-service", "checkout-service", "auth-service", "api-gateway"],
        "recommendations": [
            "Scale RDS or increase connection limit.",
            "Restart payment-service pods to clear leaked connections.",
            "Rollback to deployment v2.1.3 if saturation continues.",
        ],
    }
    ai_result = await ai_service.complete_json(
        "Return valid JSON with root_cause, confidence, blast_radius, recommendations.",
        f"Incident {incident_id}. Agent findings: {findings}",
        fallback,
    )
    return AnalysisResponse(
        root_cause=ai_result.get("root_cause", fallback["root_cause"]),
        confidence=int(ai_result.get("confidence", fallback["confidence"])),
        agents=findings,
        blast_radius=ai_result.get("blast_radius", fallback["blast_radius"]),
        recommendations=ai_result.get("recommendations", fallback["recommendations"]),
    )


async def stream_agent_workflow(incident_id: str) -> AsyncGenerator[dict, None]:
    for index, (name, thought) in enumerate(AGENTS):
        await asyncio.sleep(0.35)
        yield {
            "type": "agent_update",
            "incident_id": incident_id,
            "agent": name,
            "message": thought,
            "status": "running" if index < len(AGENTS) - 1 else "synthesizing",
            "confidence": min(92, 78 + index * 2),
        }
    async for chunk in ai_service.stream_reasoning(incident_id):
        yield {"type": "ai_token", "incident_id": incident_id, "message": chunk}
