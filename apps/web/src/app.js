import {
  agents,
  incidents,
  memory,
  metrics,
  predictions,
  radarSignals,
  recommendations,
  replayEvents,
  services,
  timeline,
} from "./data.js";

const state = {
  activeView: "overview",
  selectedIncident: incidents[0],
  chat: [
    { role: "assistant", text: "TITANIC Sentinel online. Incident context loaded for checkout-service." },
    { role: "user", text: "Why is checkout failing?" },
    { role: "assistant", text: "Checkout is failing because payment-service cannot connect to RDS. The pool is exhausted after deployment v2.1.4 introduced a connection leak." },
  ],
  replayStep: 3,
  autonomy: false,
  tick: 0,
  liveEvents: [
    "SSE standby: backend event stream will attach when FastAPI is running.",
    "Telemetry simulator active in local demo mode.",
  ],
};

const navItems = [
  ["overview", "Overview"],
  ["incidents", "Incidents"],
  ["services", "Services"],
  ["radar", "Risk Radar"],
  ["assistant", "AI Assistant"],
  ["postmortem", "Postmortems"],
  ["settings", "Settings"],
];

const $ = (selector) => document.querySelector(selector);

function cls(...names) {
  return names.filter(Boolean).join(" ");
}

function sparkline(points, tone = "ok") {
  const max = Math.max(...points);
  const min = Math.min(...points);
  const coords = points
    .map((point, index) => {
      const x = (index / (points.length - 1)) * 100;
      const y = 42 - ((point - min) / Math.max(max - min, 1)) * 34;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
  return `<svg viewBox="0 0 100 44" preserveAspectRatio="none" aria-hidden="true">
    <polyline class="sparkline sparkline-${tone}" points="${coords}"></polyline>
  </svg>`;
}

function badge(text, tone = "neutral") {
  return `<span class="badge badge-${tone}">${text}</span>`;
}

function renderShell() {
  const app = $("#app");
  app.innerHTML = `
    <div class="shell">
      <aside class="sidebar">
        <div class="brand">
          <div class="brand-mark"></div>
          <div>
            <strong>TITANIC</strong>
            <span>Autonomous Infrastructure Intelligence</span>
          </div>
        </div>
        <nav class="nav">${navItems.map(([id, label]) => `<button class="${cls("nav-item", state.activeView === id && "active")}" data-view="${id}">${label}</button>`).join("")}</nav>
        <div class="system-card">
          <div class="status-row"><span class="dot dot-ok"></span><strong>System Status</strong></div>
          <p>All mission services connected</p>
        </div>
        <div class="upgrade-card">
          <strong>Beyond monitoring <span>AI</span></strong>
          <p>Infrastructure that thinks for itself.</p>
          <button data-view="settings">Configure</button>
        </div>
      </aside>
      <main class="workspace">
        <header class="topbar">
          <div class="search">Search incidents, services, logs, metrics... <kbd>Ctrl K</kbd></div>
          <div class="top-actions">
            <button class="icon-btn" title="Alerts">AL</button>
            <button class="icon-btn" title="Theme">FX</button>
            <div class="profile"><span>AD</span><div><strong>Arjun Dev</strong><small>SRE Engineer</small></div></div>
          </div>
        </header>
        <div class="view" id="view"></div>
      </main>
    </div>
  `;
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeView = button.dataset.view;
      render();
    });
  });
}

function renderHeroIncident() {
  const incident = state.selectedIncident;
  return `
    <section class="incident-hero">
      <div class="severity">${incident.severity}</div>
      <div>
        <h1>${incident.title}</h1>
        <p>${incident.id} <span></span> ${incident.startedAt} <span></span> ${incident.duration}</p>
      </div>
      <div class="hero-actions">
        ${badge(incident.status, "danger")}
        <button class="primary-btn" id="new-incident">New Incident</button>
      </div>
      <div class="command-strip">
        <span>AI Runtime Active</span>
        <span>RCA ${incident.confidence}%</span>
        <span>Autonomy ${state.autonomy ? "Armed" : "Recommend Only"}</span>
        <span>Live Tick ${String(state.tick).padStart(2, "0")}</span>
      </div>
    </section>
  `;
}

function renderOverview() {
  return `
    ${renderHeroIncident()}
    <section class="grid primary-grid">
      ${renderRootCause()}
      ${renderTimeline()}
      ${renderServiceMap()}
      ${renderLiveStream()}
      ${renderAgentStream()}
      ${renderAnomalyRadar()}
      ${renderMetrics()}
      ${renderRecommendations()}
      ${renderChat()}
      ${renderRecentIncidents()}
      ${renderRiskRadar()}
    </section>
  `;
}

function renderLiveStream() {
  return `
    <article class="panel live-stream">
      <div class="panel-title"><h2>Realtime Event Stream</h2><span>${state.streamConnected ? "Connected" : "Demo fallback"}</span></div>
      <div class="event-feed">
        ${state.liveEvents.slice(-6).map((event) => `<p>${event}</p>`).join("")}
      </div>
    </article>
  `;
}

function renderScenarioSwitcher() {
  return `
    <article class="panel scenario-panel">
      <div class="panel-title"><h2>Mock Incident Scenarios</h2><span>Demo engine</span></div>
      <div class="scenario-list">
        ${incidents.map((incident) => `
          <button class="${cls("scenario-btn", state.selectedIncident.id === incident.id && "active")}" data-incident="${incident.id}">
            <strong>${incident.title}</strong>
            <span>${incident.severity} / ${incident.status}</span>
          </button>`).join("")}
      </div>
    </article>
  `;
}

function renderRootCause() {
  const incident = state.selectedIncident;
  return `
    <article class="panel root-cause">
      <div class="panel-title"><h2>AI Root Cause</h2><span>AI Confidence ${badge(`${incident.confidence}%`, "ok")}</span></div>
      <h3>${incident.rootCause.replace("payment-service", "<em>payment-service</em>")}</h3>
      <p class="muted">Why this happened?</p>
      <ul class="check-list">${incident.checks.map((item) => `<li>${item}</li>`).join("")}</ul>
      <div class="chips">${incident.affected.map((item) => badge(item, item.includes("payment") || item.includes("database") ? "danger" : "warn")).join("")}</div>
    </article>
  `;
}

function renderTimeline() {
  return `
    <article class="panel timeline-panel">
      <div class="panel-title"><h2>Incident Timeline</h2><span>Live</span></div>
      <ol class="timeline">${timeline.map((event, index) => `
        <li class="${event.tone}">
          <time>${event.time}</time>
          <div><strong>${event.title}</strong><small>${event.detail || ""}</small></div>
          <span>${event.source}</span>
        </li>`).join("")}</ol>
      <button class="ghost-btn" data-view="incidents">View Full Timeline</button>
    </article>
  `;
}

function renderServiceMap() {
  const lines = services.flatMap((service) => service.deps.map((dep) => {
    const target = services.find((item) => item.id === dep);
    return `<line x1="${service.x}" y1="${service.y}" x2="${target.x}" y2="${target.y}" class="edge edge-${target.risk}"></line>`;
  })).join("");
  const nodes = services.map((service) => `
    <button class="node node-${service.risk}" style="left:${service.x}%; top:${service.y}%;" title="${service.name}">
      <strong>${service.name}</strong><small>${service.health}%</small>
    </button>`).join("");
  return `
    <article class="panel service-map cinematic-map">
      <div class="panel-title"><h2>Service Map</h2><span>Live</span></div>
      <div class="map-canvas">
        <svg viewBox="0 0 100 100" preserveAspectRatio="none">${lines}</svg>
        ${nodes}
        <div class="blast-radius radius-${replayEvents[state.replayStep % replayEvents.length].node}"></div>
      </div>
      <div class="legend">
        <span><i class="dot dot-ok"></i>Healthy</span><span><i class="dot dot-warn"></i>Degraded</span><span><i class="dot dot-danger"></i>Down</span>
      </div>
    </article>
  `;
}

function renderAgentStream() {
  return `
    <article class="panel agent-stream">
      <div class="panel-title"><h2>Multi-Agent Thinking Stream</h2><span>Autonomous</span></div>
      <div class="agent-stream-list">
        ${agents.map((agent, index) => `
          <div class="thinking-card" style="--delay:${index * 90}ms">
            <div class="thinking-head">
              <strong>${agent.name}</strong>
              ${badge(agent.status, agent.status === "Complete" ? "ok" : agent.status === "Running" ? "warn" : "neutral")}
            </div>
            <p>${agent.thought}</p>
            <div class="confidence-line"><span style="width:${agent.confidence}%"></span></div>
          </div>`).join("")}
      </div>
    </article>
  `;
}

function renderAnomalyRadar() {
  const size = 210;
  const center = size / 2;
  const maxRadius = 78;
  const points = radarSignals.map((signal, index) => {
    const angle = -Math.PI / 2 + (index / radarSignals.length) * Math.PI * 2;
    const radius = (signal.value / 100) * maxRadius;
    return `${center + Math.cos(angle) * radius},${center + Math.sin(angle) * radius}`;
  }).join(" ");

  return `
    <article class="panel anomaly-radar">
      <div class="panel-title"><h2>Predictive Risk Radar</h2><span>Failure forecast</span></div>
      <div class="radar-wrap">
        <svg viewBox="0 0 ${size} ${size}" aria-label="Risk radar">
          <circle cx="${center}" cy="${center}" r="78"></circle>
          <circle cx="${center}" cy="${center}" r="52"></circle>
          <circle cx="${center}" cy="${center}" r="26"></circle>
          <polygon points="${points}"></polygon>
          ${radarSignals.map((signal, index) => {
            const angle = -Math.PI / 2 + (index / radarSignals.length) * Math.PI * 2;
            return `<text x="${center + Math.cos(angle) * 98}" y="${center + Math.sin(angle) * 98}">${signal.label}</text>`;
          }).join("")}
        </svg>
        <div>
          ${radarSignals.map((signal) => `<div class="radar-row"><span>${signal.label}</span><strong>${signal.value}%</strong></div>`).join("")}
        </div>
      </div>
    </article>
  `;
}

function renderMetrics() {
  return `
    <article class="panel metrics">
      <div class="panel-title"><h2>Metrics Overview</h2><span>24h</span></div>
      ${metrics.map((metric) => `
        <div class="metric-row">
          <div><span>${metric.label}</span><strong>${metric.value}</strong></div>
          <div class="metric-chart">${sparkline(metric.points, metric.tone)}</div>
          <small>${metric.unit}</small>
        </div>`).join("")}
    </article>
  `;
}

function renderRecommendations() {
  return `
    <article class="panel recommendations">
      <div class="panel-title"><h2>AI Recommended Actions</h2><span>Ranked</span></div>
      <ol>${recommendations.map((item, index) => `
        <li>
          <span>${index + 1}</span>
          <p>${item.label}</p>
          ${badge(item.impact, item.impact.startsWith("High") ? "danger" : item.impact.startsWith("Medium") ? "warn" : "ok")}
        </li>`).join("")}</ol>
      <button class="primary-btn wide" id="execute-fix">${state.autonomy ? "Recovery Workflow Armed" : "Execute Recommended Fix"}</button>
    </article>
  `;
}

function renderChat() {
  return `
    <article class="panel chat-panel">
      <div class="panel-title"><h2>AI Assistant Chat</h2><button class="icon-btn compact" title="Tune context">CT</button></div>
      <div class="messages">${state.chat.map((msg) => `<div class="message ${msg.role}">${msg.text}</div>`).join("")}</div>
      <form id="chat-form" class="chat-input">
        <input name="query" autocomplete="off" placeholder="Ask anything about this incident..." />
        <button type="submit">Send</button>
      </form>
    </article>
  `;
}

function renderRecentIncidents() {
  return `
    <article class="panel table-panel span-2">
      <div class="panel-title"><h2>Recent Incidents</h2><span>Memory aware</span></div>
      <table>
        <thead><tr><th>ID</th><th>Title</th><th>Severity</th><th>Status</th><th>Duration</th><th>Start Time</th></tr></thead>
        <tbody>${incidents.map((item) => `<tr><td>${item.id}</td><td>${item.title}</td><td>${badge(item.severity, item.severity === "SEV-1" ? "danger" : "warn")}</td><td>${badge(item.status, item.status === "Resolved" ? "ok" : "danger")}</td><td>${item.duration}</td><td>${item.startedAt}</td></tr>`).join("")}</tbody>
      </table>
    </article>
  `;
}

function renderRiskRadar() {
  return `
    <article class="panel radar-panel">
      <div class="panel-title"><h2>Engineering Risk Radar</h2><span>Predictive</span></div>
      ${predictions.map((item) => `
        <div class="risk-row">
          <div><strong>${item.service}</strong><small>${item.reason}</small></div>
          <meter min="0" max="100" value="${item.risk}"></meter>
          <span>${item.window}</span>
        </div>`).join("")}
      <div class="memory-box">${memory.map((item) => `<p>${item}</p>`).join("")}</div>
    </article>
  `;
}

function renderIncidentsView() {
  const replay = replayEvents[state.replayStep % replayEvents.length];
  return `
    ${renderHeroIncident()}
    <section class="grid detail-grid">
      ${renderScenarioSwitcher()}
      ${renderTimeline()}
      <article class="panel replay">
        <div class="panel-title"><h2>AI Incident Replay</h2><span>Step ${state.replayStep + 1}/${timeline.length}</span></div>
        <div class="replay-stage replay-${replay.node}">
          <div class="shockwave"></div>
          <strong>${replay.label}: ${timeline[state.replayStep].title}</strong>
          <p>${replay.detail}</p>
          <meter min="0" max="100" value="${replay.intensity}"></meter>
        </div>
        <input id="replay-slider" type="range" min="0" max="${timeline.length - 1}" value="${state.replayStep}" />
      </article>
      ${renderAgentStream()}
      ${renderRecommendations()}
      ${renderRootCause()}
    </section>
  `;
}

function renderServicesView() {
  return `
    <section class="page-title"><h1>Infrastructure Intelligence Graph</h1><p>Dependency topology, service DNA, and blast-radius simulation.</p></section>
    <section class="grid detail-grid">
      ${renderServiceMap()}
      <article class="panel service-list">
        <div class="panel-title"><h2>Service Reliability Scores</h2><span>Learning</span></div>
        ${services.map((service) => `
          <div class="service-row">
            <div><strong>${service.name}</strong><small>${service.type}</small></div>
            <span>${service.health}%</span>
            ${badge(service.risk, service.risk === "healthy" ? "ok" : service.risk === "degraded" ? "warn" : "danger")}
          </div>`).join("")}
      </article>
      ${renderRiskRadar()}
      ${renderAnomalyRadar()}
      ${renderMetrics()}
    </section>
  `;
}

function renderAssistantView() {
  return `
    <section class="page-title"><h1>Neural Core</h1><p>Chief SRE agent orchestration, memory retrieval, and recovery approval.</p></section>
    <section class="grid detail-grid">
      ${renderChat()}
      ${renderLiveStream()}
      <article class="panel agent-panel">
        <div class="panel-title"><h2>Multi-Agent Investigation</h2><span>LangGraph ready</span></div>
        ${["Log Intelligence", "Metrics", "Deployment", "Kubernetes", "Security", "Recovery", "Chief SRE"].map((agent, index) => `
          <div class="agent-row"><span>${String(index + 1).padStart(2, "0")}</span><strong>${agent} Agent</strong><small>${index < 5 ? "Complete" : index === 5 ? "Running" : "Synthesizing"}</small></div>`).join("")}
      </article>
      ${renderAgentStream()}
      ${renderRootCause()}
      ${renderRecommendations()}
    </section>
  `;
}

function renderPostmortemView() {
  return `
    <section class="page-title"><h1>Auto Postmortem</h1><p>Generated from timeline, service graph, agent evidence, and memory layer.</p></section>
    <article class="panel postmortem">
      <div class="panel-title"><h2>${state.selectedIncident.title}</h2>${badge("Draft Ready", "ok")}</div>
      <div class="postmortem-grid">
        <section><h3>Summary</h3><p>Checkout failures affected active users for ${state.selectedIncident.duration}. TITANIC identified database pool exhaustion in payment-service as the primary root cause.</p></section>
        <section><h3>Impact</h3><p>Estimated 12% checkout traffic failed. Payment authorization and auth token refresh saw cascading timeout pressure.</p></section>
        <section><h3>Root Cause</h3><p>${state.selectedIncident.rootCause}</p></section>
        <section><h3>Prevention</h3><p>Add pool leak tests, staged canary gates, connection saturation alerts, and automated rollback when RDS connections exceed 90% for 3 minutes.</p></section>
      </div>
      <button class="primary-btn">Export Postmortem</button>
    </article>
  `;
}

function renderSettingsView() {
  return `
    <section class="page-title"><h1>Integration Settings</h1><p>Connect telemetry, source control, cloud automation, and AI providers.</p></section>
    <section class="grid detail-grid">
      ${["OpenAI API", "Kubernetes", "Prometheus", "Grafana", "Datadog", "GitHub", "Neo4j", "Qdrant"].map((name, index) => `
        <article class="panel integration-card">
          <div class="panel-title"><h2>${name}</h2>${badge(index < 2 ? "Required" : "Optional", index < 2 ? "danger" : "neutral")}</div>
          <p>${integrationCopy(name)}</p>
          <button class="ghost-btn">Configure</button>
        </article>`).join("")}
    </section>
  `;
}

function integrationCopy(name) {
  const copy = {
    "OpenAI API": "Used by the multi-agent RCA, chat, postmortem, and recovery recommendation engine.",
    Kubernetes: "Needed for pod inspection, rollbacks, scaling, restarts, and self-healing approval workflows.",
    Prometheus: "Metrics source for CPU, memory, saturation, latency, and SLO anomaly detection.",
    Grafana: "Dashboard and alert context import for incident evidence.",
    Datadog: "Logs, traces, APM service maps, and anomaly signals.",
    GitHub: "Deployment and commit correlation for risky release detection.",
    Neo4j: "Infrastructure knowledge graph for dependency and blast-radius reasoning.",
    Qdrant: "Vector memory store for previous incidents and organizational reliability intelligence.",
  };
  return copy[name];
}

function renderActiveView() {
  if (state.activeView === "incidents") return renderIncidentsView();
  if (state.activeView === "services") return renderServicesView();
  if (state.activeView === "radar") return `<section class="page-title"><h1>Predictive Reliability</h1><p>Failure windows, deployment confidence, and service DNA anomalies.</p></section><section class="grid detail-grid">${renderAnomalyRadar()}${renderRiskRadar()}${renderMetrics()}${renderServiceMap()}${renderRecommendations()}</section>`;
  if (state.activeView === "assistant") return renderAssistantView();
  if (state.activeView === "postmortem") return renderPostmortemView();
  if (state.activeView === "settings") return renderSettingsView();
  return renderOverview();
}

function bindInteractions() {
  const chatForm = $("#chat-form");
  if (chatForm) {
    chatForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const query = new FormData(chatForm).get("query")?.toString().trim();
      if (!query) return;
      state.chat.push({ role: "user", text: query });
      state.chat.push({ role: "assistant", text: getAssistantReply(query) });
      chatForm.reset();
      render();
    });
  }

  const execute = $("#execute-fix");
  if (execute) {
    execute.addEventListener("click", () => {
      const approved = window.confirm("Approve dry-run recovery workflow? TITANIC will not execute production changes unless backend policy allows it.");
      if (!approved) return;
      state.autonomy = !state.autonomy;
      state.chat.push({
        role: "assistant",
        text: state.autonomy
          ? "Recovery workflow is armed. Awaiting human approval before Kubernetes or database actions are executed."
          : "Recovery workflow returned to recommendation-only mode.",
      });
      render();
    });
  }

  const slider = $("#replay-slider");
  if (slider) {
    slider.addEventListener("input", (event) => {
      state.replayStep = Number(event.target.value);
      render();
    });
  }

  document.querySelectorAll("[data-incident]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedIncident = incidents.find((incident) => incident.id === button.dataset.incident) || incidents[0];
      state.chat.push({ role: "assistant", text: `Loaded scenario ${state.selectedIncident.id}: ${state.selectedIncident.title}.` });
      render();
    });
  });
}

function getAssistantReply(query) {
  const text = query.toLowerCase();
  if (text.includes("rollback")) return "Rollback is recommended if scaling RDS cannot complete inside the next 3 minutes. The previous deployment v2.1.3 has a clean reliability signature.";
  if (text.includes("risk")) return "Highest risk is payment-service at 86%. The learned DNA profile shows abnormal connection churn and retry amplification.";
  if (text.includes("postmortem")) return "A postmortem draft is ready with summary, impact, root cause, timeline, and prevention actions.";
  return "The active evidence points to deployment v2.1.4, payment-service connection leaks, and RDS max connection saturation. Recommended first action is scale RDS or restart payment-service pods after approval.";
}

function render() {
  renderShell();
  $("#view").innerHTML = renderActiveView();
  bindInteractions();
}

render();

function connectEventStream() {
  if (!window.EventSource) return;
  const source = new EventSource(`http://127.0.0.1:8000/events/incident/${state.selectedIncident.id}`);
  source.onopen = () => {
    state.streamConnected = true;
    state.liveEvents.push("Connected to TITANIC realtime backend stream.");
    render();
  };
  source.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.type === "agent_update") {
        state.liveEvents.push(`${payload.agent}: ${payload.message}`);
      } else if (payload.type === "telemetry") {
        const critical = payload.metrics?.find((metric) => metric.status === "critical");
        state.liveEvents.push(`Telemetry: ${critical?.service || "system"} ${critical?.metric || "health"} streaming.`);
      } else if (payload.message) {
        state.liveEvents.push(payload.message);
      }
      render();
    } catch {
      state.liveEvents.push(event.data);
    }
  };
  source.onerror = () => {
    state.streamConnected = false;
    source.close();
  };
}

connectEventStream();

setInterval(() => {
  state.tick = (state.tick + 1) % 100;
  document.querySelectorAll(".metric-row strong").forEach((item, index) => {
    if (index === 0) item.textContent = `${(22 + Math.sin(state.tick / 3) * 3).toFixed(1)}%`;
    if (index === 1) item.textContent = `${(2.2 + Math.cos(state.tick / 4) * 0.3).toFixed(2)}s`;
  });
  const liveTick = document.querySelector(".command-strip span:last-child");
  if (liveTick) liveTick.textContent = `Live Tick ${String(state.tick).padStart(2, "0")}`;
}, 1200);
