from typing import Protocol

from pydantic import BaseModel, Field


class VectorStoreRecord(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    embedding: list[float] | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class VectorStoreQuery(BaseModel):
    query: str
    embedding: list[float] | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class VectorStore(Protocol):
    async def upsert_chunks(self, records: list[VectorStoreRecord]) -> None:
        """Persist chunks and embeddings in a future implementation."""

    async def search(self, query: VectorStoreQuery) -> list[VectorStoreRecord]:
        """Search vector-backed chunks in a future implementation."""


class PlaceholderVectorStore:
    async def upsert_chunks(self, records: list[VectorStoreRecord]) -> None:
        # TODO: Manually implement pgvector writes after embeddings are available.
        raise NotImplementedError("Manual vector store writes are not implemented yet.")

    async def search(self, query: VectorStoreQuery) -> list[VectorStoreRecord]:
        # TODO: Manually implement pgvector similarity search.
        raise NotImplementedError("Manual vector search is not implemented yet.")
