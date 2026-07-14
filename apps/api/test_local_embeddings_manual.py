from __future__ import annotations

import asyncio

from app.rag.embeddings import EmbeddingInput, LocalSentenceTransformerEmbeddingProvider
from app.rag.vector_store import cosine_similarity


async def main() -> None:
    provider = LocalSentenceTransformerEmbeddingProvider(
        model_name="intfloat/multilingual-e5-small",
        batch_size=8,
    )

    vectors = await provider.embed(
        [
            EmbeddingInput(
                text="pressure oscillation under load",
                metadata={"input_type": "query"},
            ),
            EmbeddingInput(
                text="hydraulic pressure instability during machine operation",
                metadata={"input_type": "passage"},
            ),
            EmbeddingInput(
                text="Vue component state management with Pinia",
                metadata={"input_type": "passage"},
            ),
        ]
    )

    query = vectors[0]
    similar = vectors[1]
    unrelated = vectors[2]

    similar_score = cosine_similarity(query.vector, similar.vector)
    unrelated_score = cosine_similarity(query.vector, unrelated.vector)

    print(f"Model: {query.model}")
    print(f"Dimensions: {len(query.vector)}")
    print(f"Similar score: {similar_score:.6f}")
    print(f"Unrelated score: {unrelated_score:.6f}")

    assert similar_score > unrelated_score

    print("✅ Local embedding semantic similarity test passed.")


if __name__ == "__main__":
    asyncio.run(main())