# TITANIC Validation Report

Validation date: 2026-05-24

## Passed

- Frontend served on `http://localhost:5173`.
- Backend served on `http://127.0.0.1:8000`.
- CORS allows `http://localhost:5173`.
- Favicon returns HTTP 200.
- Browser console showed no errors/warnings during navigation and chat smoke test.
- Navigation works:
  - Overview
  - Incidents
  - Services
  - Risk Radar
  - AI Assistant
  - Postmortems
  - Settings
- AI Assistant chat accepts input and returns a response.
- Realtime Event Stream panel renders.
- SSE endpoint streams agent reasoning.
- Backend pytest suite passed: 5 tests.
- API smoke endpoints returned HTTP 200:
  - `/health`
  - `/incidents`
  - `/incidents/INC-4821`
  - `/incidents/INC-4821/timeline`
  - `/services`
  - `/metrics`
  - `/topology`
  - `/topology/blast-radius/db`
  - `/replay/INC-4821`
  - `/ai/predictions`
  - `/memory/similar`
  - `/ai/analyze`
  - `/ai/chat`
  - `/ai/postmortem`
  - `/recovery/plan`
  - `/recovery/execute`
  - `/auth/login`

## Dependency Connectivity

- API: ok
- Frontend: ok
- OpenAI: configured
- Postgres: degraded locally due password mismatch for user `titanic`
- Redis: degraded unless local stack is running
- Neo4j: degraded unless local stack is running
- Qdrant: degraded unless local stack is running
- Docker Desktop Linux engine: not running during validation

## Important Behavior

`/recovery/execute` correctly blocks execution without human approval and returns dry-run safe output. This is the expected safe behavior.

