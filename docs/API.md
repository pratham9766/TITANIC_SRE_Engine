# TITANIC API Surface

## Health

- `GET /health`
- `GET /system/health`
- `POST /auth/login`

## Incidents

- `GET /incidents`
- `GET /incidents/{incident_id}`
- `GET /incidents/{incident_id}/timeline`

## AI

- `POST /ai/analyze`
- `POST /ai/chat`
- `POST /ai/postmortem`
- `GET /ai/predictions`

## Infrastructure

- `GET /topology`
- `POST /topology/sync`
- `GET /topology/blast-radius/{service_id}`
- `GET /services`
- `GET /metrics`

## Replay

- `GET /replay/{incident_id}`

## Recovery

- `POST /recovery/plan`
- `POST /recovery/execute`

## Realtime

- `GET /events/incident/{incident_id}` returns Server-Sent Events for agent reasoning and telemetry.

## Memory

- `GET /memory/similar?q=...`
- `POST /memory/remember/{incident_id}?summary=...`

Endpoints return real provider data when configured and fall back to deterministic demo data when external systems are unavailable.
