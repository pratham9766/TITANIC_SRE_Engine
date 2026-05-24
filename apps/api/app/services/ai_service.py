from __future__ import annotations

import json
from collections.abc import AsyncGenerator

from app.config import settings
from app.services.prompts import CHAT_SYSTEM_PROMPT, RCA_SYSTEM_PROMPT


class AIService:
    def __init__(self) -> None:
        self.enabled = bool(settings.openai_api_key)
        self.model = settings.openai_model

    async def complete_json(self, system: str, user: str, fallback: dict) -> dict:
        if not self.enabled:
            return fallback
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)
        except Exception:
            return fallback

    async def complete_text(self, message: str, context: str) -> str:
        fallback = (
            "The evidence points to payment-service connection exhaustion after deployment v2.1.4. "
            "Recommended next step: scale database capacity or restart payment pods after approval."
        )
        if not self.enabled:
            return fallback
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": CHAT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{message}"},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content or fallback
        except Exception:
            return fallback

    async def stream_reasoning(self, incident_id: str) -> AsyncGenerator[str, None]:
        if not self.enabled:
            for chunk in [
                "Metrics Agent: analyzing latency spikes...",
                "Deployment Agent: correlating deployment v2.1.4...",
                "Topology Agent: tracing blast radius...",
                "Chief SRE Agent: generating final RCA...",
            ]:
                yield chunk
            return

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            stream = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": RCA_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Stream short multi-agent reasoning updates for {incident_id}."},
                ],
                stream=True,
                temperature=0.25,
            )
            async for event in stream:
                delta = event.choices[0].delta.content
                if delta:
                    yield delta
        except Exception:
            yield "Chief SRE Agent: AI provider unavailable, using deterministic incident model."


ai_service = AIService()
