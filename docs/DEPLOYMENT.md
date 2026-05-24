# TITANIC Deployment Notes

## Local Backend

```powershell
cd apps/api
.\scripts\setup_backend.ps1
uvicorn app.main:app --reload --port 8000
```

Run migrations after Postgres is available:

```powershell
alembic upgrade head
```

## Local Infrastructure

```powershell
cd infra
docker compose up --build
```

## Frontend

The current demo can run without a build:

```powershell
python -m http.server 4173 -d apps/web
```

React/Vite migration scaffold is present for the production frontend:

```powershell
cd apps/web
npm install
npm run dev
```

## Suggested Hosting

- Frontend: Vercel
- Backend: Railway or Render
- Postgres: Railway, Neon, Supabase, or Render
- Redis: Upstash or Railway
- Neo4j: Neo4j Aura
- Qdrant: Qdrant Cloud
