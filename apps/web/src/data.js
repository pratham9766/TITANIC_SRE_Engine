export const services = [
  { id: "web", name: "Web Portal", type: "frontend", health: 99.1, risk: "healthy", x: 10, y: 42, deps: ["gateway"] },
  { id: "gateway", name: "API Gateway", type: "edge", health: 95.9, risk: "healthy", x: 29, y: 42, deps: ["auth", "checkout", "payment"] },
  { id: "auth", name: "Auth Service", type: "service", health: 86.6, risk: "degraded", x: 47, y: 18, deps: ["db"] },
  { id: "checkout", name: "Checkout Service", type: "service", health: 9.3, risk: "down", x: 58, y: 42, deps: ["payment", "inventory"] },
  { id: "payment", name: "Payment Service", type: "service", health: 52.4, risk: "down", x: 47, y: 65, deps: ["db"] },
  { id: "inventory", name: "Inventory Service", type: "service", health: 98.4, risk: "healthy", x: 78, y: 65, deps: [] },
  { id: "db", name: "Database RDS", type: "database", health: 0.9, risk: "down", x: 52, y: 84, deps: [] },
];

export const incidents = [
  {
    id: "INC-4821",
    title: "Checkout Service Outage",
    severity: "SEV-1",
    status: "Active",
    duration: "38m 42s",
    startedAt: "May 20, 2025 12:07 PM",
    confidence: 92,
    rootCause: "Database connection pool exhaustion in payment-service causing cascade failures in downstream services.",
    affected: ["payment-service", "checkout-service", "auth-service", "database-rds"],
    checks: [
      "Deployment v2.1.4 increased DB connections by 230%",
      "Connection leaks detected in PaymentService.java:87",
      "RDS instance hit max connections at 500/500",
      "Auth and Checkout services failed due to timeouts",
    ],
  },
  {
    id: "INC-4820",
    title: "Search Service High Latency",
    severity: "SEV-2",
    status: "Resolved",
    duration: "21m 14s",
    startedAt: "May 19, 2025 10:21 PM",
    confidence: 88,
    rootCause: "Cache miss storm after index rebuild caused elevated p95 latency.",
    affected: ["search-service", "redis-cache"],
    checks: ["Index rebuild completed", "Cache warmed", "Latency returned under SLO"],
  },
  {
    id: "INC-4822",
    title: "Redis Timeout Cascade",
    severity: "SEV-2",
    status: "Investigating",
    duration: "11m 08s",
    startedAt: "May 20, 2025 01:14 PM",
    confidence: 84,
    rootCause: "Redis shard saturation caused auth token validation delays and gateway retry amplification.",
    affected: ["redis-cache", "auth-service", "api-gateway"],
    checks: [
      "Redis p99 latency crossed 890ms",
      "Gateway retry policy amplified auth traffic by 4.2x",
      "Cache eviction jumped above learned baseline",
      "No suspicious security pattern detected",
    ],
  },
  {
    id: "INC-4823",
    title: "Kubernetes Pod Crash Loop",
    severity: "SEV-2",
    status: "Mitigating",
    duration: "18m 31s",
    startedAt: "May 20, 2025 02:02 PM",
    confidence: 89,
    rootCause: "A memory limit regression caused checkout-worker pods to crash loop during traffic spikes.",
    affected: ["checkout-worker", "kubernetes-node-07", "api-gateway"],
    checks: [
      "OOMKilled events detected on node-07",
      "Memory requests changed in latest Helm release",
      "Traffic burst aligned with crash loop start time",
      "Horizontal autoscaler could not stabilize replicas",
    ],
  },
  {
    id: "INC-4824",
    title: "API Latency Explosion",
    severity: "SEV-1",
    status: "Active",
    duration: "07m 46s",
    startedAt: "May 20, 2025 02:44 PM",
    confidence: 91,
    rootCause: "Gateway thread pool saturation is causing cascading timeout pressure across downstream services.",
    affected: ["api-gateway", "auth-service", "checkout-service"],
    checks: [
      "Gateway p95 latency crossed 4.8s",
      "Thread pool queue depth reached 96%",
      "Downstream services are healthy but timeout-bound",
      "Traffic surge exceeds current autoscaling window",
    ],
  },
  {
    id: "INC-4825",
    title: "Deployment Regression",
    severity: "SEV-3",
    status: "Resolved",
    duration: "26m 03s",
    startedAt: "May 20, 2025 03:09 PM",
    confidence: 93,
    rootCause: "A feature flag rollout changed checkout validation behavior and increased 4xx responses.",
    affected: ["checkout-service", "feature-flags", "web-portal"],
    checks: [
      "4xx errors started 90 seconds after flag rollout",
      "No infrastructure saturation detected",
      "Rollback restored baseline behavior",
      "Postmortem prevention item generated",
    ],
  },
];

export const timeline = [
  { time: "12:01 PM", tone: "ok", title: "Deployment v2.1.4 started", source: "github-actions" },
  { time: "12:03 PM", tone: "ok", title: "DB connections spiked", source: "RDS", detail: "543 -> 498 (+230%)" },
  { time: "12:05 PM", tone: "warn", title: "High latency detected", source: "Datadog", detail: "payment-service p95 crossed 2.4s" },
  { time: "12:06 PM", tone: "danger", title: "Payment service errors increased", source: "Datadog", detail: "5xx rate breached 24%" },
  { time: "12:07 PM", tone: "danger", title: "Checkout failures begin", source: "Grafana", detail: "User impact detected" },
  { time: "12:08 PM", tone: "danger", title: "Auth service timeouts increased", source: "Datadog" },
];

export const metrics = [
  { label: "Error Rate", value: "24.8%", unit: "30%", tone: "danger", points: [3, 24, 14, 17, 12, 15, 11, 21, 27, 9, 16, 25, 24, 23, 22] },
  { label: "Latency p95", value: "2.45s", unit: "3s", tone: "warn", points: [6, 14, 9, 8, 12, 7, 17, 22, 10, 12, 26, 29, 25, 24, 20] },
  { label: "DB Connections", value: "498 / 500", unit: "500", tone: "danger", points: [9, 12, 11, 19, 22, 31, 38, 29, 35, 41, 45, 48, 49, 50, 50] },
  { label: "CPU Usage", value: "78%", unit: "100%", tone: "ok", points: [20, 24, 31, 26, 28, 33, 39, 34, 29, 37, 42, 41, 48, 45, 47] },
];

export const recommendations = [
  { label: "Scale RDS instance or increase connection limit", impact: "High Impact", risk: "low", action: "scale-rds" },
  { label: "Restart payment-service pods to clear leaked connections", impact: "High Impact", risk: "medium", action: "restart-payment" },
  { label: "Rollback to previous deployment v2.1.3", impact: "Medium Impact", risk: "medium", action: "rollback" },
  { label: "Add connection pool monitoring and alerts", impact: "Low Impact", risk: "low", action: "monitoring" },
];

export const predictions = [
  { service: "payment-service", risk: 86, window: "Next 45m", reason: "Connection churn remains above learned baseline" },
  { service: "checkout-service", risk: 74, window: "Next 2h", reason: "Downstream retries are amplifying traffic" },
  { service: "auth-service", risk: 42, window: "Tonight", reason: "Timeouts correlate with database saturation" },
];

export const memory = [
  "Similar DB exhaustion incident detected 2 times in the last 30 days.",
  "Payment service normally holds 120 to 150 DB sessions; current signature is 498.",
  "Deployments touching PaymentService.java historically require a staged canary.",
];

export const agents = [
  {
    name: "Metrics Agent",
    status: "Complete",
    thought: "Detected DB connection saturation, error-rate spike, and payment-service retry storm.",
    confidence: 94,
  },
  {
    name: "Deployment Agent",
    status: "Complete",
    thought: "Matched failure onset to deployment v2.1.4 and isolated PaymentService.java connection changes.",
    confidence: 91,
  },
  {
    name: "Log Agent",
    status: "Complete",
    thought: "Found repeated connection acquisition timeout errors and leaked session warnings.",
    confidence: 88,
  },
  {
    name: "Security Agent",
    status: "Complete",
    thought: "No attack pattern found. Traffic shape matches retry amplification, not abuse.",
    confidence: 81,
  },
  {
    name: "Topology Agent",
    status: "Running",
    thought: "Tracing blast radius from database to payment, checkout, auth, and gateway.",
    confidence: 86,
  },
  {
    name: "Recovery Agent",
    status: "Planning",
    thought: "Preparing safe options: scale RDS, restart payment pods, or rollback deployment.",
    confidence: 83,
  },
  {
    name: "Chief SRE Agent",
    status: "Synthesizing",
    thought: "Combining evidence into final RCA with confidence and approval-gated recovery plan.",
    confidence: 92,
  },
];

export const replayEvents = [
  { label: "Deploy", detail: "v2.1.4 shipped to payment-service", node: "payment", intensity: 24 },
  { label: "Leak", detail: "Connection sessions fail to close", node: "payment", intensity: 48 },
  { label: "Saturation", detail: "RDS max connections reached", node: "db", intensity: 82 },
  { label: "Cascade", detail: "Checkout and auth timeouts begin", node: "checkout", intensity: 94 },
  { label: "Recovery", detail: "Scale and restart workflow prepared", node: "gateway", intensity: 58 },
];

export const radarSignals = [
  { label: "Outage", value: 86 },
  { label: "Memory", value: 72 },
  { label: "Scaling", value: 81 },
  { label: "Traffic", value: 64 },
  { label: "Deploy", value: 92 },
  { label: "Security", value: 28 },
];
