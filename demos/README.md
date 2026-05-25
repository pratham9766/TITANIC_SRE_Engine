# TITANIC Demo Pack

This folder contains reusable scripts and talking points for showing TITANIC as a hackathon/investor demo.

## Recommended Demo URLs

- Frontend: http://localhost:5173
- Backend health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs
- Realtime stream: http://127.0.0.1:8000/events/incident/INC-4821

## Demo Order

1. Open Mission Control.
2. Show the active checkout outage and AI confidence.
3. Open AI Assistant and ask: `Should we rollback payment service?`
4. Open Incidents and show replay mode.
5. Select Redis timeout and Kubernetes crash scenarios.
6. Open Services and show topology/blast radius.
7. Open Risk Radar and explain predictive reliability.
8. Open Postmortems and show generated incident report.
9. Run `.\demos\api_smoke_test.ps1` to prove the backend is real.

## Best Demo Line

“This is not monitoring. This is autonomous infrastructure intelligence: TITANIC detects, investigates, explains, recommends, and safely prepares recovery.”

