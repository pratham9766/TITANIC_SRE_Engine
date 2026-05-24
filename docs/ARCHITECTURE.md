# TITANIC Scalable Architecture

## Product Modules

1. **Mission Control UI**
   - Active incidents, live health, AI summaries, telemetry charts, and recovery progress.
   - Current implementation: `apps/web`.

2. **Telemetry Ingestion Layer**
   - Sources: logs, metrics, traces, deployments, Kubernetes events, cloud events, GitHub commits, user-impact signals.
   - Production stack: OpenTelemetry Collector, Fluent Bit, Prometheus remote write, Kafka or Redpanda.

3. **Event Correlation Engine**
   - Normalizes time-series events, detects anomalies, creates incident candidates, and stitches timelines.
   - Production stack: FastAPI workers, Redis Streams, Postgres, background task queue.

4. **Multi-Agent AI Engine**
   - Agents: Log Intelligence, Metrics, Deployment, Kubernetes, Security, Recovery, Chief SRE.
   - Production stack: LangGraph with OpenAI API. CrewAI can be used for demo orchestration, but LangGraph is better for durable, inspectable workflows.

5. **Infrastructure Knowledge Graph**
   - Stores services, dependencies, ownership, deploy history, blast radius, and failure relationships.
   - Production stack: Neo4j.

6. **Vector Memory Layer**
   - Stores incident summaries, RCA evidence, postmortems, runbooks, deployment risks, and service DNA profiles.
   - Production stack: Qdrant for local/self-hosted or Pinecone for managed SaaS.

7. **Recovery Automation Engine**
   - Human-approved or policy-approved operations: scale, restart, rollback, reroute, clear queue, quarantine service.
   - Production stack: Kubernetes API, ArgoCD, GitHub Actions, cloud SDKs.

8. **Postmortem and Learning Loop**
   - Generates postmortems, updates memory, improves reliability scores, and records prevention actions.

## Data Flow

```text
Telemetry Sources
  -> Ingestion Pipeline
  -> Event Correlation Engine
  -> Incident Candidate
  -> Multi-Agent AI Investigation
  -> Chief SRE Synthesis
  -> Dashboard, Chat, Recovery Recommendation
  -> Approved Automation
  -> Postmortem and Memory Update
```

## Backend Boundaries

- `routers/incidents.py` - incident list, detail, and timeline.
- `routers/ai.py` - RCA, chat, predictions, postmortem generation.
- `routers/topology.py` - services and dependency graph.
- `routers/recovery.py` - recovery action proposals and approvals.
- `services/ai_engine.py` - OpenAI/LangGraph orchestration boundary.
- `services/telemetry.py` - telemetry simulator now, real collectors later.
- `services/recovery.py` - Kubernetes/ArgoCD execution boundary.

## Database Model

Core tables:

- `users`
- `organizations`
- `services`
- `incidents`
- `telemetry_events`
- `deployments`
- `ai_analysis`
- `recovery_actions`
- `knowledge_memory`

Graph nodes:

- `Service`
- `Deployment`
- `Incident`
- `Alert`
- `Runbook`
- `Owner`

Graph relationships:

- `DEPENDS_ON`
- `CAUSED_BY`
- `AFFECTED`
- `DEPLOYED_TO`
- `SIMILAR_TO`
- `MITIGATED_BY`

## Scaling Plan

- Use Kafka or Redpanda partitions by organization and service ID.
- Keep raw telemetry in object storage or observability backends; store normalized evidence in Postgres.
- Run AI analysis as async jobs with workflow IDs and stream status over WebSockets.
- Cache active incident state in Redis.
- Keep vector memory per organization with strict tenant isolation.
- Put recovery execution behind RBAC, policy checks, audit logs, and human approval by default.

## Security Model

- Organization-level tenancy.
- RBAC roles: Viewer, Responder, SRE Admin, Automation Admin.
- Encrypted secrets via cloud KMS or Vault.
- Audit every AI recommendation and recovery action.
- Require signed approvals for destructive or production-changing operations.
- Never send raw secrets or credentials to AI prompts.

## AI Prompting Strategy

- Retrieval first: pull service topology, last deployments, metrics anomalies, related incidents, runbooks, and logs.
- Agent isolation: each agent returns evidence and confidence, not final conclusions.
- Chief SRE synthesis: combines evidence, produces RCA, confidence, blast radius, and action plan.
- Recovery agent: proposes actions with risk, rollback path, commands, and approval requirements.
- Memory write: summarize only validated incident facts after resolution.

## Production Roadmap

1. MVP: mock telemetry, AI RCA, service graph, chat, postmortem.
2. V2: Prometheus, GitHub, Kubernetes read-only integration.
3. V3: Neo4j graph, Qdrant memory, Datadog/Grafana integrations.
4. V4: approved self-healing automation with ArgoCD and Kubernetes.
5. V5: predictive scaling, chaos simulation, service DNA profiling, executive mode.

