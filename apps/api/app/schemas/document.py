from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentKind(StrEnum):
    manual = "manual"
    maintenance_log = "maintenance_log"
    sop = "sop"
    incident_report = "incident_report"


class Document(BaseModel):
    id: str
    name: str
    kind: DocumentKind
    machine_id: str | None
    uploaded_at: datetime
    status: str
    source_uri: str | None = None
    sections: list[str] = Field(default_factory=list)


class IngestDocumentRequest(BaseModel):
    name: str
    kind: DocumentKind
    machine_id: str | None = None
    source_uri: str | None = None


class IngestDocumentResponse(BaseModel):
    status: str
    document_name: str
    message: str


DocumentSummary = Document
