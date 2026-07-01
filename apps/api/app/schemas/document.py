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
    title: str | None = None
    name: str
    kind: DocumentKind
    source_type: str | None = None
    file_path: str | None = None
    domain: str | None = None
    machine_type: str | None = None
    created_at: datetime | None = None
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
    domain: str | None = None
    machine_type: str | None = None


class IngestDocumentResponse(BaseModel):
    run_id: str
    status: str
    document_name: str
    documents_processed: int
    chunks_created: int
    message: str


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    section_title: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    embedding: list[float] | None = None
    created_at: datetime
    is_placeholder: bool = True


class DocumentIngestionRun(BaseModel):
    id: str
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    documents_processed: int = 0
    chunks_created: int = 0
    error_message: str | None = None


DocumentSummary = Document
