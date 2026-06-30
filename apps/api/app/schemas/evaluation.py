from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    case_id: str
    incident_input: str
    expected_error_codes: list[str] = Field(default_factory=list)
    expected_retrieved_documents: list[str] = Field(default_factory=list)
    expected_root_causes: list[str] = Field(default_factory=list)
    expected_safety_notes: list[str] = Field(default_factory=list)
    should_require_human_confirmation: bool
