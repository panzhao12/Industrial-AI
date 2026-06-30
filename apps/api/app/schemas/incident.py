from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.diagnosis import (
    AnalysisStatus,
    DiagnosisCause,
    DiagnosisEvidence,
    DiagnosisRecommendation,
    DiagnosisResult,
)


class IncidentSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class IncidentStatus(StrEnum):
    open = "open"
    investigating = "investigating"
    mitigated = "mitigated"
    closed = "closed"


class IncidentTimelineEvent(BaseModel):
    occurred_at: datetime
    label: str
    description: str


class Incident(BaseModel):
    id: str
    machine_id: str
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    opened_at: datetime
    owner: str
    description: str
    symptoms: list[str] = Field(default_factory=list)
    error_codes: list[str] = Field(default_factory=list)
    telemetry_summary: str | None = None
    root_cause: str | None = None
    actions_taken: list[str] = Field(default_factory=list)
    outcome: str | None = None
    downtime_hours: float | None = None
    related_manual_sections: list[str] = Field(default_factory=list)
    timeline: list[IncidentTimelineEvent] = Field(default_factory=list)


class AnalyzeIncidentRequest(BaseModel):
    operator_notes: str | None = None
    requested_by: str | None = None


IncidentSummary = Incident
IncidentDetail = Incident

__all__ = [
    "AnalysisStatus",
    "AnalyzeIncidentRequest",
    "DiagnosisCause",
    "DiagnosisEvidence",
    "DiagnosisRecommendation",
    "DiagnosisResult",
    "Incident",
    "IncidentDetail",
    "IncidentSeverity",
    "IncidentStatus",
    "IncidentSummary",
    "IncidentTimelineEvent",
]
