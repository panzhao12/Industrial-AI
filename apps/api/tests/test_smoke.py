from fastapi.testclient import TestClient
import pytest

from app.data.synthetic_loader import load_error_codes, load_repair_cases
from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_machines(client: TestClient) -> None:
    response = client.get("/machines")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_machine_current_telemetry(client: TestClient) -> None:
    response = client.get("/machines/HYD-EXC-001/telemetry/current")
    assert response.status_code == 200

    payload = response.json()
    assert payload["machine_id"] == "HYD-EXC-001"
    assert payload["summary"]
    assert len(payload["readings"]) > 0


def test_incidents(client: TestClient) -> None:
    response = client.get("/incidents")
    assert response.status_code == 200
    assert len(response.json()) >= 30


def test_incident_detail_contains_synthetic_repair_fields(client: TestClient) -> None:
    response = client.get("/incidents/RC-001")
    assert response.status_code == 200

    payload = response.json()
    assert payload["error_codes"] == ["HYD-101", "PMP-420"]
    assert payload["telemetry_summary"]
    assert payload["related_manual_sections"]


def test_documents_are_synthetic_manuals(client: TestClient) -> None:
    response = client.get("/documents")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 5
    assert payload[0]["sections"]


def test_document_detail_and_chunks(client: TestClient) -> None:
    detail_response = client.get("/documents/MAN-EXC-420H")
    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == "MAN-EXC-420H"

    chunks_response = client.get("/documents/MAN-EXC-420H/chunks")
    assert chunks_response.status_code == 200
    chunks = chunks_response.json()
    assert len(chunks) > 0
    assert chunks[0]["is_placeholder"] is True
    assert chunks[0]["embedding"] is None


def test_ingest_document_placeholder(client: TestClient) -> None:
    response = client.post(
        "/documents/ingest",
        json={
            "name": "Placeholder pump bulletin",
            "kind": "manual",
            "machine_id": "HYD-PMP-003",
            "source_uri": "file://synthetic/pump-bulletin.md",
        },
    )
    assert response.status_code == 202

    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["documents_processed"] == 0
    assert payload["chunks_created"] == 0


def test_rag_search_placeholder(client: TestClient) -> None:
    response = client.post(
        "/rag/search",
        json={"query": "pressure oscillation under load", "top_k": 5},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["is_placeholder"] is True
    assert payload["results"]
    assert payload["results"][0]["is_placeholder"] is True


def test_analyze_incident_placeholder(client: TestClient) -> None:
    response = client.post(
        "/incidents/RC-001/analyze",
        json={"operator_notes": "Smoke test only.", "requested_by": "pytest"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["incident_id"] == "RC-001"
    assert payload["status"] == "placeholder"
    assert payload["probable_causes"] == []
    assert payload["recommended_actions"] == []
    assert payload["evidence"] == []
    assert payload["human_review_required"] is True


def test_agent_trace_placeholder(client: TestClient) -> None:
    response = client.get("/agent/traces/trace-demo")
    assert response.status_code == 200

    payload = response.json()
    assert payload["is_mock"] is True
    assert [step["name"] for step in payload["steps"]] == [
        "load_incident_context",
        "detect_anomalies",
        "retrieve_manuals",
        "generate_hypotheses",
        "human_confirmation_pending",
    ]


def test_evaluation_cases(client: TestClient) -> None:
    response = client.get("/evaluation/cases")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload) >= 10
    assert payload[0]["case_id"].startswith("EVAL-")


def test_synthetic_catalog_counts() -> None:
    error_codes = load_error_codes()
    repair_cases = load_repair_cases()

    assert len(error_codes) >= 20
    assert len(repair_cases) >= 30
    assert {"HYD-101", "HYD-204", "HYD-310", "PMP-420", "ACC-505"}.issubset(
        {item.code for item in error_codes}
    )
