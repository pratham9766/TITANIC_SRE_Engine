# TITANIC AI SRE Engineer

TITANIC is an AI-native reliability operating system prototype for autonomous incident investigation, predictive reliability, infrastructure intelligence, and recovery workflows.

## What Is Included

- `apps/web` - runnable command center UI with incident RCA, service map, replay, chat, postmortem, and integration settings.
- `apps/api` - FastAPI-ready backend scaffold for incidents, topology, AI analysis, chat, recovery, and predictions.
- `docs/ARCHITECTURE.md` - scalable product architecture mapped to the blueprint.
- `docs/MANUAL_SETUP.md` - required API keys, links, cloud settings, and integration notes.
- `docs/API.md` - endpoint contract for incidents, AI, infrastructure, replay, and recovery.
- `infra/docker-compose.yml` - local service plan for Postgres, Redis, Neo4j, and Qdrant.
- `apps/api/alembic` - SQLAlchemy/Alembic schema migration setup.

## Run The Demo UI

From the workspace root:

```powershell
python -m http.server 4173 -d apps/web
```

Open:

```text
http://localhost:4173
```

The current UI is self-contained and uses realistic mock telemetry so the product can be reviewed before real integrations are connected.

## Frontend Stack Scaffold

The instant demo is no-build for hackathon reliability. The React/Vite/Tailwind migration scaffold is also included in `apps/web/package.json`, `vite.config.ts`, and `tailwind.config.ts`.

After Node dependencies are available:

```powershell
cd apps/web
npm install
npm run dev
```

## Run The API Later

```powershell
cd apps/api
.\scripts\setup_backend.ps1
uvicorn app.main:app --reload --port 8000
```

Create `apps/api/.env` from `.env.example` before enabling real AI and infrastructure actions.

Run full local infra:

```powershell
cd infra
docker compose up --build
```
