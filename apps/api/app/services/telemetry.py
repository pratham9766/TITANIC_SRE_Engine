from app.schemas import Incident, ReplayEvent, ServiceNode, TelemetryMetric, TimelineEvent


def active_incidents() -> list[Incident]:
    return [
        Incident(
            id="INC-4821",
            title="Checkout Service Outage",
            severity="SEV-1",
            status="Active",
            duration="38m 42s",
            confidence=92,
            root_cause="Database connection pool exhaustion in payment-service causing cascade failures.",
            affected_services=["payment-service", "checkout-service", "auth-service", "database-rds"],
        )
    ]


def get_incident(incident_id: str) -> Incident:
    for incident in active_incidents():
        if incident.id == incident_id:
            return incident
    return active_incidents()[0]


def incident_timeline(incident_id: str) -> list[TimelineEvent]:
    return [
        TimelineEvent(time="12:01 PM", title="Deployment v2.1.4 started", source="github-actions", severity="info"),
        TimelineEvent(time="12:03 PM", title="DB connections spiked", source="RDS", severity="warning", detail="543 -> 498"),
        TimelineEvent(time="12:06 PM", title="Payment service errors increased", source="Datadog", severity="critical"),
        TimelineEvent(time="12:07 PM", title="Checkout failures begin", source="Grafana", severity="critical"),
    ]


def topology() -> list[ServiceNode]:
    return [
        ServiceNode(id="gateway", name="API Gateway", kind="edge", health=95.9, risk="healthy", depends_on=["auth", "checkout"]),
        ServiceNode(id="checkout", name="Checkout Service", kind="service", health=9.3, risk="down", depends_on=["payment"]),
        ServiceNode(id="payment", name="Payment Service", kind="service", health=52.4, risk="down", depends_on=["db"]),
        ServiceNode(id="db", name="Database RDS", kind="database", health=0.9, risk="down"),
    ]


def services() -> list[ServiceNode]:
    return topology()


def metrics() -> list[TelemetryMetric]:
    return [
        TelemetryMetric(service="payment-service", metric="error_rate", value=24.8, unit="percent", status="critical"),
        TelemetryMetric(service="payment-service", metric="latency_p95", value=2.45, unit="seconds", status="critical"),
        TelemetryMetric(service="database-rds", metric="connections", value=498, unit="connections", status="critical"),
        TelemetryMetric(service="api-gateway", metric="cpu", value=78, unit="percent", status="warning"),
    ]


def replay(incident_id: str) -> list[ReplayEvent]:
    return [
        ReplayEvent(index=0, label="Deploy", detail="v2.1.4 shipped to payment-service", affected_node="payment", intensity=24),
        ReplayEvent(index=1, label="Leak", detail="Connection sessions fail to close", affected_node="payment", intensity=48),
        ReplayEvent(index=2, label="Saturation", detail="RDS max connections reached", affected_node="db", intensity=82),
        ReplayEvent(index=3, label="Cascade", detail="Checkout and auth timeouts begin", affected_node="checkout", intensity=94),
        ReplayEvent(index=4, label="Recovery", detail="Scale and restart workflow prepared", affected_node="gateway", intensity=58),
    ]
