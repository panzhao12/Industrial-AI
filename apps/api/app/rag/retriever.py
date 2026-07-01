from typing import Protocol

from pydantic import BaseModel, Field


class RetrievalQuery(BaseModel):
    query: str
    machine_id: str | None = None
    incident_id: str | None = None
    limit: int = Field(default=5, ge=1, le=25)


class RetrievedChunk(BaseModel):
    document_id: str
    chunk_id: str
    source_name: str
    text: str
    score: float
    metadata: dict[str, str] = Field(default_factory=dict)


class RagRetriever(Protocol):
    async def retrieve(self, query: RetrievalQuery) -> list[RetrievedChunk]:
        """Retrieve relevant chunks for future diagnosis workflows."""


class PlaceholderRagRetriever:
    async def retrieve(self, query: RetrievalQuery) -> list[RetrievedChunk]:
        # TODO: Manually compose vector, lexical, and metadata retrieval later.
        raise NotImplementedError("Manual RAG retrieval is not implemented yet.")
