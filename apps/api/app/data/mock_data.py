from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.agent_trace import AgentTrace, AgentTraceStep
from app.schemas.diagnosis import Diagnosis
from app.schemas.document import Document, DocumentChunk, IngestDocumentRequest, IngestDocumentResponse
from app.schemas.evaluation import EvaluationCase
from app.schemas.incident import Incident
from app.schemas.machine import Machine, TelemetrySnapshot
from app.schemas.rag import RagSearchResult

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


def get_document(document_id: str) -> Document | None:
    return next((document for document in load_documents() if document.id == document_id), None)


def list_document_chunks(document_id: str) -> list[DocumentChunk]:
    document = get_document(document_id)
    if document is None:
        return []

    now = datetime.now(UTC)
    sections = document.sections or ["Synthetic metadata preview"]
    return [
        DocumentChunk(
            id=f"{document.id}-chunk-{index:03d}",
            document_id=document.id,
            chunk_index=index,
            section_title=section,
            content=(
                f"Placeholder chunk preview for {section}. "
                "The general document API has not parsed or indexed this record. "
                "Local RAG ingestion is available through the /rag endpoints."
            ),
            metadata={
                "source": "synthetic_manual_metadata",
                "document_title": document.title or document.name,
                "machine_id": document.machine_id or "",
                "domain": document.domain or "",
            },
            embedding=None,
            created_at=now,
            is_placeholder=True,
        )
        for index, section in enumerate(sections)
    ]


def build_placeholder_ingestion_response(
    payload: IngestDocumentRequest,
) -> IngestDocumentResponse:
    return IngestDocumentResponse(
        run_id=f"ingest-{uuid4()}",
        status="accepted",
        document_name=payload.name,
        documents_processed=0,
        chunks_created=0,
        message=(
            "Document ingestion placeholder accepted the request. "
            "No file loading, parsing, chunking, embeddings, or vector writes ran."
        ),
    )


def search_placeholder_chunks(query: str, top_k: int) -> list[RagSearchResult]:
    chunks: list[DocumentChunk] = []
    for document in load_documents():
        chunks.extend(list_document_chunks(document.id))

    results: list[RagSearchResult] = []
    for index, chunk in enumerate(chunks[:top_k]):
        document = get_document(chunk.document_id)
        results.append(
            RagSearchResult(
                document_id=chunk.document_id,
                document_title=(document.title or document.name) if document else chunk.document_id,
                chunk_id=chunk.id,
                chunk_index=chunk.chunk_index,
                section_title=chunk.section_title,
                content=chunk.content,
                score=round(0.25 - (index * 0.01), 3),
                metadata={
                    **chunk.metadata,
                    "query": query,
                    "retrieval_mode": "placeholder_no_similarity_search",
                },
                is_placeholder=True,
            )
        )
    return results


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
