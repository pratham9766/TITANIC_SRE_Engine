from __future__ import annotations

import math
import time

import httpx

from app.config import settings
from app.schemas import TelemetryMetric
from app.services.telemetry import metrics as demo_metrics


class TelemetryHub:
    async def current_metrics(self) -> list[TelemetryMetric]:
        prometheus = await self._prometheus_metrics()
        if prometheus:
            return prometheus
        return self._simulated_metrics()

    async def _prometheus_metrics(self) -> list[TelemetryMetric]:
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                response = await client.get(f"{settings.prometheus_url}/api/v1/query", params={"query": "up"})
                response.raise_for_status()
            return [
                TelemetryMetric(service="prometheus", metric="up", value=1, unit="bool", status="healthy"),
                *demo_metrics(),
            ]
        except Exception:
            return []

    def _simulated_metrics(self) -> list[TelemetryMetric]:
        wave = math.sin(time.time() / 5)
        return [
            TelemetryMetric(service="payment-service", metric="error_rate", value=24.8 + wave * 3, unit="percent", status="critical"),
            TelemetryMetric(service="payment-service", metric="latency_p95", value=2.45 + wave * 0.25, unit="seconds", status="critical"),
            TelemetryMetric(service="database-rds", metric="connections", value=498 + wave, unit="connections", status="critical"),
            TelemetryMetric(service="api-gateway", metric="cpu", value=78 + wave * 6, unit="percent", status="warning"),
        ]


telemetry_hub = TelemetryHub()
