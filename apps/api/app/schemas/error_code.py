from pydantic import BaseModel, Field


class ErrorCode(BaseModel):
    code: str
    title: str
    severity: str
    description: str
    likely_causes: list[str] = Field(default_factory=list)
    recommended_checks: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
