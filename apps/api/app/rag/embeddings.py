from __future__ import annotations

import hashlib
import math
from collections.abc import Sequence
from typing import Any, Protocol

from pydantic import BaseModel, Field

from app.rag.schemas import DocumentChunk, EmbeddedChunk


class EmbeddingInput(BaseModel):
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmbeddingVector(BaseModel):
    text: str
    vector: list[float]
    model: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmbeddingProvider(Protocol):
    async def embed(self, inputs: Sequence[EmbeddingInput]) -> list[EmbeddingVector]:
        """Create embeddings for future document chunks or queries."""


class FakeEmbeddingProvider:
    """
    Deterministic fake embedding provider for local development.

    This does NOT create real semantic embeddings.
    It only creates stable numeric vectors so the rest of the RAG pipeline
    can be built and tested before connecting a real embedding provider.
    """

    def __init__(self, dimensions: int = 1536, model_name: str = "fake-hash-embedding") -> None:
        self.dimensions = dimensions
        self.model_name = model_name

    async def embed(self, inputs: Sequence[EmbeddingInput]) -> list[EmbeddingVector]:
        results: list[EmbeddingVector] = []

        for item in inputs:
            if not item.text.strip():
                raise ValueError("Cannot embed empty text.")

            raw_vector = self._hash_text_to_vector(item.text)
            normalized_vector = self._normalize(raw_vector)

            results.append(
                EmbeddingVector(
                    text=item.text,
                    vector=normalized_vector,
                    model=self.model_name,
                    metadata=item.metadata,
                )
            )

        return results

    def _hash_text_to_vector(self, text: str) -> list[float]:
        values: list[float] = []
        counter = 0

        while len(values) < self.dimensions:
            raw = f"{text}:{counter}".encode("utf-8")
            digest = hashlib.sha256(raw).digest()

            for byte in digest:
                value = (byte / 127.5) - 1.0
                values.append(value)

                if len(values) >= self.dimensions:
                    break

            counter += 1

        return values

    def _normalize(self, vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(value * value for value in vector))

        if norm == 0:
            return vector

        return [value / norm for value in vector]


class LocalSentenceTransformerEmbeddingProvider:
    """
    Real local embedding provider using sentence-transformers.

    Default model:
    - intfloat/multilingual-e5-small

    This runs locally and does not require OpenAI or Gemini API.
    """

    def __init__(
        self,
        model_name: str = "intfloat/multilingual-e5-small",
        batch_size: int = 32,
        normalize_embeddings: bool = True,
    ) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1.")

        # Import lazily so the app can still run with FakeEmbeddingProvider
        # even if sentence-transformers is not installed.
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self.batch_size = batch_size
        self.normalize_embeddings = normalize_embeddings
        self.model = SentenceTransformer(model_name)

    async def embed(self, inputs: Sequence[EmbeddingInput]) -> list[EmbeddingVector]:
        if not inputs:
            return []

        for item in inputs:
            if not item.text.strip():
                raise ValueError("Cannot embed empty text.")

        results: list[EmbeddingVector] = []

        for batch in _batch_embedding_inputs(list(inputs), self.batch_size):
            prepared_texts = [self._prepare_text(item) for item in batch]

            embeddings = self.model.encode(
                prepared_texts,
                batch_size=self.batch_size,
                normalize_embeddings=self.normalize_embeddings,
                convert_to_numpy=True,
                show_progress_bar=False,
            )

            for input_item, vector in zip(batch, embeddings, strict=True):
                results.append(
                    EmbeddingVector(
                        text=input_item.text,
                        vector=vector.tolist(),
                        model=self.model_name,
                        metadata=input_item.metadata,
                    )
                )

        return results

    def _prepare_text(self, item: EmbeddingInput) -> str:
        text = item.text.strip()

        # E5 models are trained with explicit prefixes.
        # Documents/passages should use "passage: ..."
        # Search queries should use "query: ..."
        if "e5" not in self.model_name.lower():
            return text

        lowered = text.lower()
        if lowered.startswith("query:") or lowered.startswith("passage:"):
            return text

        input_type = item.metadata.get("input_type")

        if input_type == "query":
            return f"query: {text}"

        return f"passage: {text}"


def _batch_embedding_inputs(
    items: list[EmbeddingInput],
    batch_size: int,
) -> list[list[EmbeddingInput]]:
    return [
        items[index : index + batch_size]
        for index in range(0, len(items), batch_size)
    ]


def create_embedding_provider(
    provider_name: str,
    local_model_name: str = "intfloat/multilingual-e5-small",
    local_batch_size: int = 32,
) -> EmbeddingProvider:
    normalized_provider = provider_name.lower().strip()

    if normalized_provider == "fake":
        return FakeEmbeddingProvider()

    if normalized_provider == "local":
        return LocalSentenceTransformerEmbeddingProvider(
            model_name=local_model_name,
            batch_size=local_batch_size,
        )

    raise ValueError(
        f"Unsupported RAG embedding provider: {provider_name}. "
        "Supported values: fake, local."
    )


async def embed_chunks(
    chunks: Sequence[DocumentChunk],
    provider: EmbeddingProvider,
) -> list[EmbeddedChunk]:
    """
    Convert document chunks into embedded chunks.

    This is the bridge between:
    DocumentChunk -> EmbeddingInput -> EmbeddingVector -> EmbeddedChunk
    """

    inputs = [
        EmbeddingInput(
            text=chunk.content,
            metadata={
                **chunk.metadata,
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "section_title": chunk.section_title or "",
                "input_type": "passage",
            },
        )
        for chunk in chunks
    ]

    vectors = await provider.embed(inputs)

    if len(vectors) != len(chunks):
        raise ValueError(
            f"Embedding provider returned {len(vectors)} vectors for {len(chunks)} chunks."
        )

    embedded_chunks: list[EmbeddedChunk] = []

    for chunk, vector in zip(chunks, vectors, strict=True):
        embedded_chunks.append(
            EmbeddedChunk(
                **chunk.model_dump(),
                embedding=vector.vector,
            )
        )

    return embedded_chunks