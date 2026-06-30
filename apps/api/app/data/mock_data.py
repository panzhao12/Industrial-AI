from datetime import UTC, datetime

from app.schemas.agent_trace import AgentTrace, AgentTraceStep
from app.schemas.diagnosis import Diagnosis
from app.schemas.document import Document
from app.schemas.evaluation import EvaluationCase
from app.schemas.incident import Incident
from app.schemas.machine import Machine, TelemetrySnapshot

from app.data.synthetic_loader import (
    load_documents,
    load_evaluation_cases,
    load_machines,
    load_repair_cases,
    load_telemetry_snapshots,
)


def list_machines() -> list[Machine]:
    return list(load_machines())


def get_machine(machine_id: str) -> Machine | None:
    return next((machine for machine in load_machines() if machine.id == machine_id), None)


def get_current_telemetry(machine_id: str) -> TelemetrySnapshot | None:
    return next(
        (
            snapshot
            for snapshot in load_telemetry_snapshots()
            if snapshot.machine_id == machine_id
        ),
        None,
    )


def list_incidents() -> list[Incident]:
    return list(load_repair_cases())


def get_incident(incident_id: str) -> Incident | None:
    return next((incident for incident in load_repair_cases() if incident.id == incident_id), None)


def list_documents() -> list[Document]:
    return list(load_documents())


def list_evaluation_cases() -> list[EvaluationCase]:
    return list(load_evaluation_cases())


def build_placeholder_diagnosis(incident_id: str) -> Diagnosis:
    return Diagnosis(
        incident_id=incident_id,
        status="placeholder",
        generated_at=datetime.now(UTC),
        summary=(
            "Diagnosis placeholder only. No LLM, RAG retriever, LangGraph workflow, "
            "embedding service, or external tool was called."
        ),
        confidence=None,
        probable_causes=[],
        recommended_actions=[],
        evidence=[],
        human_review_required=True,
        next_state="awaiting_manual_diagnosis_agent_implementation",
    )


def get_agent_trace(trace_id: str) -> AgentTrace:
    step_names = [
        "load_incident_context",
        "detect_anomalies",
        "retrieve_manuals",
        "generate_hypotheses",
        "human_confirmation_pending",
    ]
    return AgentTrace(
        trace_id=trace_id,
        incident_id="RC-001",
        is_mock=True,
        message="Mock trace data only. No agent graph, retrieval, LLM, or tool execution ran.",
        steps=[
            AgentTraceStep(
                name=name,
                status="mock",
                started_at=None,
                completed_at=None,
                detail="Mock step reserved for future manual agent implementation.",
            )
            for name in step_names
        ],
    )
