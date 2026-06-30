from pydantic import BaseModel, Field


class DiagnosisAgentState(BaseModel):
    incident_id: str
    trace_id: str | None = None
    notes: list[str] = Field(default_factory=list)
    requires_human_confirmation: bool = True
