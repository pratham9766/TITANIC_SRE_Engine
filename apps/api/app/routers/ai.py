from fastapi import APIRouter

from app.schemas import AnalysisRequest, ChatRequest, PostmortemRequest
from app.services.ai_engine import analyze_incident, answer_chat, generate_postmortem

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat")
async def chat(request: ChatRequest):
    return await answer_chat(request)


@router.post("/analyze")
async def analyze(request: AnalysisRequest):
    return await analyze_incident(request.incident_id)


@router.post("/postmortem")
async def postmortem(request: PostmortemRequest):
    return await generate_postmortem(request.incident_id)


@router.get("/predictions")
def predictions():
    return [
        {"service": "payment-service", "risk": 86, "window": "Next 45m"},
        {"service": "checkout-service", "risk": 74, "window": "Next 2h"},
        {"service": "auth-service", "risk": 42, "window": "Tonight"},
    ]
