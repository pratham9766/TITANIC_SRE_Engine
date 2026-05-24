from app.services.agent_workflow import AGENTS
from app.services.recovery_service import recovery_service
from app.services.telemetry import active_incidents, replay, topology


def test_demo_incidents_exist():
    incidents = active_incidents()
    assert incidents
    assert incidents[0].id.startswith("INC-")


def test_topology_has_dependencies():
    graph = topology()
    assert any(node.depends_on for node in graph)


def test_replay_has_cinematic_events():
    events = replay("INC-4821")
    assert events[0].label == "Deploy"
    assert max(event.intensity for event in events) >= 80


def test_recovery_defaults_to_safe_dry_run():
    plan = recovery_service.plan("restart-payment")
    assert plan.requires_approval is True
    assert plan.dry_run is True


def test_agent_workflow_has_chief_sre():
    assert any(name == "Chief SRE Agent" for name, _ in AGENTS)
