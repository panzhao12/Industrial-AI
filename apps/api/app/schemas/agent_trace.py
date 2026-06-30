from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class AgentTraceStatus(StrEnum):
    mock = "mock"
    pending = "pending"
    completed = "completed"
    failed = "failed"


class AgentTraceStep(BaseModel):
    name: str
    status: AgentTraceStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    detail: str
    inputs: dict[str, str] = Field(default_factory=dict)
    outputs: dict[str, str] = Field(default_factory=dict)


class AgentTrace(BaseModel):
    trace_id: str
    incident_id: str | None = None
    is_mock: bool
    message: str
    steps: list[AgentTraceStep] = Field(default_factory=list)
