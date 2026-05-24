# Manual Setup And Required Links

The current UI demo runs without any external keys. Real AI and infrastructure features need these manual settings.

## Required For AI Features

- OpenAI API key: create from [OpenAI Platform API Keys](https://platform.openai.com/api-keys)
- Environment variable:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1
```

Use OpenAI for:

- Multi-agent RCA
- AI chat
- Postmortem generation
- Recovery recommendation reasoning
- Incident memory summarization

## Required For Kubernetes Automation

- Kubernetes cluster access with a restricted service account.
- `KUBECONFIG` path or in-cluster service account token.
- RBAC permissions for read-only mode first:
  - `get/list/watch pods`
  - `get/list/watch deployments`
  - `get/list/watch events`
  - `get/list/watch services`
- Additional permissions for self-healing mode:
  - rollout restart
  - scale deployments
  - rollback through ArgoCD or deployment revisions

Keep destructive operations behind manual approval.

## Observability Integrations

Prometheus:

```text
PROMETHEUS_URL=http://localhost:9090
```

Grafana:

```text
GRAFANA_URL=https://your-org.grafana.net
GRAFANA_API_KEY=your_key_here
```

Datadog:

```text
DATADOG_API_KEY=your_key_here
DATADOG_APP_KEY=your_app_key_here
DATADOG_SITE=datadoghq.com
```

OpenTelemetry:

```text
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Source Control And Deployment Context

GitHub:

```text
GITHUB_TOKEN=github_pat_or_app_token
GITHUB_ORG=your_org
```

ArgoCD:

```text
ARGOCD_SERVER=https://argocd.example.com
ARGOCD_AUTH_TOKEN=your_token_here
```

## Memory And Graph Stores

Postgres:

```text
DATABASE_URL=postgresql+psycopg://titanic:titanic@localhost:5432/titanic
```

Redis:

```text
REDIS_URL=redis://localhost:6379/0
```

Neo4j:

```text
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=change_me
```

Qdrant:

```text
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

## Safety Settings

Recommended defaults:

```text
AUTONOMY_MODE=recommend_only
REQUIRE_HUMAN_APPROVAL=true
ALLOW_PRODUCTION_WRITES=false
MAX_RECOVERY_ACTIONS_PER_INCIDENT=3
RECOVERY_DRY_RUN=true
```

Do not enable production writes until RBAC, audit logs, rollback paths, and approval flows are tested.

## Demo Login

The lightweight auth service includes local demo users:

```text
admin@titanic.local / titanic-demo
viewer@titanic.local / titanic-demo
```

Change `JWT_SECRET` before any shared demo.
