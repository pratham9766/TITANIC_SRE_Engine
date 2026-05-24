from app.schemas import (
    AnalysisResponse,
    ChatRequest,
    ChatResponse,
    PostmortemResponse,
    RecoveryPlan,
)
from app.services.agent_workflow import run_agent_workflow
from app.services.ai_service import ai_service
from app.services.memory_service import memory_service
from app.services.recovery_service import recovery_service


async def answer_chat(request: ChatRequest) -> ChatResponse:
    similar = await memory_service.similar_incidents(request.message)
    context = f"incident_id={request.incident_id}; similar_incidents={similar}"
    answer = await ai_service.complete_text(request.message, context)
    return ChatResponse(
        answer=answer,
        citations=[f"memory:{item.get('incident_id')}" for item in similar],
        confidence=88,
    )


def recovery_plan(action: str) -> RecoveryPlan:
    return recovery_service.plan(action)


async def analyze_incident(incident_id: str) -> AnalysisResponse:
    analysis = await run_agent_workflow(incident_id)
    await memory_service.remember_incident(incident_id, analysis.root_cause)
    return analysis


async def generate_postmortem(incident_id: str) -> PostmortemResponse:
    fallback = {
        "title": "Checkout Service Outage Postmortem",
        "summary": "Checkout failures were triggered by payment-service database connection exhaustion.",
        "root_cause": "Deployment v2.1.4 introduced a connection leak that saturated RDS connections.",
        "impact": "Approximately 12% of checkout traffic failed during the incident window.",
        "recovery_actions": ["Scale database capacity.", "Restart payment-service pods.", "Prepare rollback to v2.1.3."],
        "prevention": ["Add connection leak tests.", "Gate deployments on pool saturation canaries.", "Alert at 80% and 90% RDS connection usage."],
    }
    result = await ai_service.complete_json(
        "Return valid JSON with title, summary, root_cause, impact, recovery_actions, prevention.",
        f"Generate a postmortem for {incident_id}.",
        fallback,
    )
    return PostmortemResponse(
        title=result.get("title", fallback["title"]),
        summary=result.get("summary", fallback["summary"]),
        root_cause=result.get("root_cause", fallback["root_cause"]),
        impact=result.get("impact", fallback["impact"]),
        recovery_actions=result.get("recovery_actions", fallback["recovery_actions"]),
        prevention=result.get("prevention", fallback["prevention"]),
    )
