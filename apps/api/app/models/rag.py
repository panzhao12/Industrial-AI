from datetime import datetime

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    id: str
    title: str
    source_type: str
    file_path: str | None = None
    domain: str | None = None
    machine_type: str | None = None
    created_at: datetime


class DocumentChunkRecord(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    section_title: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    embedding: list[float] | None = None
    created_at: datetime


class DocumentIngestionRunRecord(BaseModel):
    id: str
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    documents_processed: int = 0
    chunks_created: int = 0
    error_message: str | None = None
