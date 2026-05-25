# TITANIC Usage Guide

## Start The Frontend

```powershell
Start-Process -FilePath "C:\Users\Milind BOKEFODE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -ArgumentList "-m","http.server","5173","--bind","127.0.0.1","-d","D:\Pratham\TITANIC\apps\web" -WorkingDirectory "D:\Pratham\TITANIC" -WindowStyle Hidden
```

Open:

```text
http://localhost:5173
```

## Start The Backend

```powershell
cd D:\Pratham\TITANIC\apps\api
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Run Backend Smoke Test

```powershell
cd D:\Pratham\TITANIC
.\demos\api_smoke_test.ps1
```

## Run Realtime Agent Stream Demo

```powershell
cd D:\Pratham\TITANIC
.\demos\sse_demo.ps1
```

The SSE endpoint is intentionally long-lived. The demo script samples a few seconds and then stops.

## Run Automated Tests

```powershell
cd D:\Pratham\TITANIC
$env:PYTHONPATH="D:\Pratham\TITANIC\apps\api"
.\apps\api\.venv\Scripts\python.exe -m pytest apps\api\tests
```

## Full Dependency Stack

Docker Desktop must be running before starting the full stack:

```powershell
cd D:\Pratham\TITANIC
docker-compose -f infra\docker-compose.yml up --build
```

Then run migrations:

```powershell
cd D:\Pratham\TITANIC\apps\api
.\.venv\Scripts\alembic.exe upgrade head
```

## Current Known Environment Notes

- The app works in demo mode without Postgres, Redis, Neo4j, or Qdrant.
- Docker Desktop was not running during validation, so the full dependency stack could not be started.
- Local Postgres on `127.0.0.1:5432` rejected the configured `titanic/titanic` credentials.
- OpenAI is configured according to `/system/health`, but if the API key or network is invalid, TITANIC falls back to deterministic demo AI.

## Demo Flow

1. Open `http://localhost:5173`.
2. Show Overview and the checkout outage.
3. Open AI Assistant and ask a demo question.
4. Open Incidents and show the replay timeline.
5. Switch incident scenarios.
6. Open Services and explain blast radius.
7. Open Risk Radar and explain predictive failure.
8. Open Postmortems and show generated report.
9. Run `.\demos\api_smoke_test.ps1`.
