import json
from functools import lru_cache
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, TypeAdapter

from app.schemas.document import Document
from app.schemas.error_code import ErrorCode
from app.schemas.evaluation import EvaluationCase
from app.schemas.incident import Incident, IncidentTimelineEvent
from app.schemas.machine import Machine, TelemetrySnapshot

T = TypeVar("T", bound=BaseModel)

SYNTHETIC_DATA_ROOT = Path(__file__).resolve().parents[4] / "data" / "synthetic"


def _load_json(relative_path: str) -> object:
    with (SYNTHETIC_DATA_ROOT / relative_path).open(encoding="utf-8") as file:
        return json.load(file)


def _load_model_list(relative_path: str, model: type[T]) -> list[T]:
    adapter = TypeAdapter(list[model])
    return adapter.validate_python(_load_json(relative_path))


@lru_cache
def load_machines() -> tuple[Machine, ...]:
    return tuple(_load_model_list("machines/machines.json", Machine))


@lru_cache
def load_telemetry_snapshots() -> tuple[TelemetrySnapshot, ...]:
    return tuple(_load_model_list("telemetry/current_snapshots.json", TelemetrySnapshot))


@lru_cache
def load_error_codes() -> tuple[ErrorCode, ...]:
    return tuple(_load_model_list("error_codes/error_codes.json", ErrorCode))


@lru_cache
def load_documents() -> tuple[Document, ...]:
    return tuple(_load_model_list("manuals/manuals.json", Document))


@lru_cache
def load_repair_cases() -> tuple[Incident, ...]:
    raw_cases = _load_json("repair_cases/repair_cases.json")
    if not isinstance(raw_cases, list):
        raise ValueError("repair_cases/repair_cases.json must contain a JSON array.")

    incidents: list[Incident] = []
    for raw_case in raw_cases:
        raw = dict(raw_case)
        case_id = str(raw.pop("case_id"))
        opened_at = raw["opened_at"]
        symptoms = raw.get("symptoms", [])
        incident = Incident(
            id=case_id,
            description=raw.get("telemetry_summary", raw.get("title", "")),
            timeline=[
                IncidentTimelineEvent(
                    occurred_at=opened_at,
                    label="Synthetic repair case opened",
                    description="Loaded from data/synthetic/repair_cases/repair_cases.json.",
                )
            ],
            **raw,
        )
        if not incident.description and symptoms:
            incident.description = symptoms[0]
        incidents.append(incident)
    return tuple(incidents)


@lru_cache
def load_evaluation_cases() -> tuple[EvaluationCase, ...]:
    return tuple(_load_model_list("evaluation/evaluation_cases.json", EvaluationCase))
