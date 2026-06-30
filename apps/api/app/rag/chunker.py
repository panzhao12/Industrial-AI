from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel, Field


class ChunkingInput(BaseModel):
    document_id: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentChunker(Protocol):
    def chunk(self, inputs: Sequence[ChunkingInput]) -> list[DocumentChunk]:
        """Split documents into chunks for future retrieval."""


class PlaceholderDocumentChunker:
    def chunk(self, inputs: Sequence[ChunkingInput]) -> list[DocumentChunk]:
        raise NotImplementedError("Manual RAG chunking is not implemented yet.")
