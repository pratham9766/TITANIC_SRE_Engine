from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ai, auth, events, incidents, infrastructure, memory, recovery, replay, system, topology

app = FastAPI(title="TITANIC AI SRE API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents.router)
app.include_router(topology.router)
app.include_router(infrastructure.router)
app.include_router(ai.router)
app.include_router(recovery.router)
app.include_router(replay.router)
app.include_router(events.router)
app.include_router(system.router)
app.include_router(auth.router)
app.include_router(memory.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "titanic-api"}
