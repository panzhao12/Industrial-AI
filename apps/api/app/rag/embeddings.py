from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel, Field


class EmbeddingInput(BaseModel):
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


class EmbeddingVector(BaseModel):
    text: str
    vector: list[float]
    model: str
    metadata: dict[str, str] = Field(default_factory=dict)


class EmbeddingProvider(Protocol):
    async def embed(self, inputs: Sequence[EmbeddingInput]) -> list[EmbeddingVector]:
        """Create embeddings for future document chunks or queries."""


class PlaceholderEmbeddingProvider:
    async def embed(self, inputs: Sequence[EmbeddingInput]) -> list[EmbeddingVector]:
        # TODO: Manually wire a selected embedding provider after the RAG design is approved.
        raise NotImplementedError("Manual embedding provider integration is not implemented yet.")
