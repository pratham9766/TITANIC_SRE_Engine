from pydantic import BaseModel, Field


class Incident(BaseModel):
    id: str
    title: str
    severity: str
    status: str
    duration: str
    confidence: int = Field(ge=0, le=100)
    root_cause: str
    affected_services: list[str]


class TelemetryMetric(BaseModel):
    service: str
    metric: str
    value: float
    unit: str
    status: str


class ReplayEvent(BaseModel):
    index: int
    label: str
    detail: str
    affected_node: str
    intensity: int = Field(ge=0, le=100)


class AnalysisRequest(BaseModel):
    incident_id: str


class AnalysisResponse(BaseModel):
    root_cause: str
    confidence: int = Field(ge=0, le=100)
    agents: list[dict]
    recommendations: list[str]
    blast_radius: list[str] = []


class PostmortemRequest(BaseModel):
    incident_id: str


class PostmortemResponse(BaseModel):
    title: str
    summary: str
    root_cause: str
    impact: str
    recovery_actions: list[str]
    prevention: list[str]


class TimelineEvent(BaseModel):
    time: str
    title: str
    source: str
    severity: str
    detail: str | None = None


class ServiceNode(BaseModel):
    id: str
    name: str
    kind: str
    health: float
    risk: str
    depends_on: list[str] = []


class ChatRequest(BaseModel):
    incident_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[str] = []
    confidence: int = Field(ge=0, le=100)


class RecoveryRequest(BaseModel):
    incident_id: str
    action: str
    approved_by: str | None = None
    approval_token: str | None = None


class RecoveryPlan(BaseModel):
    action: str
    risk: str
    requires_approval: bool
    command_preview: str
    rollback_plan: str
    dry_run: bool = True
    status: str = "planned"


class RecoveryExecution(BaseModel):
    incident_id: str
    action: str
    status: str
    dry_run: bool
    audit_id: str
    output: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SystemHealth(BaseModel):
    api: str
    database: dict
    redis: dict
    neo4j: dict
    qdrant: dict
    openai: dict
