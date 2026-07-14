from __future__ import annotations

from pathlib import Path

from app.rag.chunker import MarkdownChunker
from app.rag.document_loader import load_markdown_folder
from app.core.config import settings
from app.rag.embeddings import create_embedding_provider, embed_chunks
from app.rag.retriever import VectorRagRetriever
from app.rag.schemas import RetrievalQuery, RetrievalResult
from app.rag.vector_store import InMemoryVectorStore


embedding_provider = create_embedding_provider(
    provider_name=settings.rag_embedding_provider,
    local_model_name=settings.local_embedding_model,
    local_batch_size=settings.local_embedding_batch_size,
)
vector_store = InMemoryVectorStore()
retriever = VectorRagRetriever(
    embedding_provider=embedding_provider,
    vector_store=vector_store,
)


async def ingest_local_manuals(manuals_path: Path) -> dict[str, int]:
    documents = await load_markdown_folder(str(manuals_path))

    chunker = MarkdownChunker()
    all_chunks = []

    for document in documents:
        chunking_result = chunker.chunk(document)
        all_chunks.extend(chunking_result.chunks)

    embedded_chunks = await embed_chunks(all_chunks, embedding_provider)

    await retriever.index_chunks(embedded_chunks)

    return {
        "documents": len(documents),
        "chunks": len(all_chunks),
        "embedded_chunks": len(embedded_chunks),
        "stored_records": vector_store.count(),
    }


async def search(query: RetrievalQuery) -> RetrievalResult:
    return await retriever.retrieve(query)


def get_rag_status() -> dict[str, int | str]:
    return {
        "embedding_provider": embedding_provider.__class__.__name__,
        "embedding_model": getattr(embedding_provider, "model_name", "unknown"),
        "vector_store": "InMemoryVectorStore",
        "stored_records": vector_store.count(),
    }


def clear_rag_index() -> dict[str, int]:
    vector_store.clear()
    return {
        "stored_records": vector_store.count(),
    }