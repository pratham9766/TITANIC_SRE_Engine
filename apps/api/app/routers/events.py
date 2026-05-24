import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.agent_workflow import stream_agent_workflow
from app.services.telemetry_adapters import telemetry_hub

router = APIRouter(prefix="/events", tags=["events"])


async def _event(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


@router.get("/incident/{incident_id}")
async def incident_events(incident_id: str):
    async def stream():
        async for update in stream_agent_workflow(incident_id):
            yield await _event(update)
        while True:
            metrics = [metric.model_dump() for metric in await telemetry_hub.current_metrics()]
            yield await _event({"type": "telemetry", "incident_id": incident_id, "metrics": metrics})
            await asyncio.sleep(2)

    return StreamingResponse(stream(), media_type="text/event-stream")
