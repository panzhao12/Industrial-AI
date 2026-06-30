from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DiagnosisStatus(StrEnum):
    placeholder = "placeholder"
    queued = "queued"
    completed = "completed"
    failed = "failed"


class DiagnosisCause(BaseModel):
    label: str
    rationale: str
    confidence: float | None = Field(default=None, ge=0, le=1)


class DiagnosisRecommendation(BaseModel):
    action: str
    priority: str
    safety_note: str | None = None


class DiagnosisEvidence(BaseModel):
    source: str
    reference: str
    excerpt: str


class Diagnosis(BaseModel):
    incident_id: str
    status: DiagnosisStatus
    generated_at: datetime
    summary: str
    confidence: float | None = Field(default=None, ge=0, le=1)
    probable_causes: list[DiagnosisCause] = Field(default_factory=list)
    recommended_actions: list[DiagnosisRecommendation] = Field(default_factory=list)
    evidence: list[DiagnosisEvidence] = Field(default_factory=list)
    human_review_required: bool
    next_state: str


DiagnosisResult = Diagnosis
AnalysisStatus = DiagnosisStatus
