from typing import Protocol

from pydantic import BaseModel, Field


class DocumentLoadRequest(BaseModel):
    source_uri: str
    source_type: str
    metadata: dict[str, str] = Field(default_factory=dict)


class LoadedDocument(BaseModel):
    title: str
    content: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentLoader(Protocol):
    async def load(self, request: DocumentLoadRequest) -> LoadedDocument:
        """Load a source document for future ingestion."""


class PlaceholderDocumentLoader:
    async def load(self, request: DocumentLoadRequest) -> LoadedDocument:
        # TODO: Manually implement file/object-store loading during the real RAG phase.
        raise NotImplementedError("Manual document loading is not implemented yet.")
