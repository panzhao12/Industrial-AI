from __future__ import annotations

import asyncio
from pathlib import Path

from app.rag.chunker import MarkdownChunker
from app.rag.document_loader import load_markdown_folder
from app.rag.embeddings import FakeEmbeddingProvider, embed_chunks
from app.rag.retriever import VectorRagRetriever
from app.rag.schemas import RetrievalQuery
from app.rag.vector_store import InMemoryVectorStore


async def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    manuals_path = project_root / "data" / "synthetic" / "manuals"

    print(f"Loading manuals from: {manuals_path}")

    documents = await load_markdown_folder(str(manuals_path))

    if not documents:
        raise RuntimeError("No markdown documents found.")

    chunker = MarkdownChunker()
    embedding_provider = FakeEmbeddingProvider()
    vector_store = InMemoryVectorStore()

    all_chunks = []

    for document in documents:
        chunking_result = chunker.chunk(document)
        all_chunks.extend(chunking_result.chunks)

    if not all_chunks:
        raise RuntimeError("No chunks were created. Check your markdown files or chunker settings.")

    embedded_chunks = await embed_chunks(all_chunks, embedding_provider)

    retriever = VectorRagRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    await retriever.index_chunks(embedded_chunks)

    target_chunk = embedded_chunks[0]

    print("\nTarget chunk:")
    print(f"Chunk ID: {target_chunk.id}")
    print(f"Document ID: {target_chunk.document_id}")
    print(f"Section: {target_chunk.section_title}")
    print(target_chunk.content[:300])

    result = await retriever.retrieve(
        RetrievalQuery(
            query=target_chunk.content,
            top_k=3,
        )
    )

    print("\nSearch results:")

    for index, item in enumerate(result.results, start=1):
        print("-" * 80)
        print(f"Rank: {index}")
        print(f"Score: {item.score:.6f}")
        print(f"Chunk ID: {item.chunk_id}")
        print(f"Document: {item.document_title}")
        print(f"Section: {item.section_title}")
        print(item.content[:300])

    top_result = result.results[0]

    assert top_result.chunk_id == target_chunk.id, (
        f"Expected top result chunk_id {target_chunk.id}, "
        f"but got {top_result.chunk_id}"
    )

    assert top_result.score > 0.999, (
        f"Expected score close to 1.0, but got {top_result.score}"
    )

    print("\n[OK] Self-match retrieval test passed.")


if __name__ == "__main__":
    asyncio.run(main())