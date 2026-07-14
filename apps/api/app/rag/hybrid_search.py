from typing import Protocol

from app.rag.schemas import RetrievedChunk, RetrievalQuery


class HybridSearch(Protocol):
    async def search(self, query: RetrievalQuery) -> list[RetrievedChunk]:
        """Combine lexical and vector search in a future implementation."""


class PlaceholderHybridSearch:
    async def search(self, query: RetrievalQuery) -> list[RetrievedChunk]:
        # TODO: Manually implement lexical/vector fusion once retrieval behavior is defined.
        raise NotImplementedError("Manual hybrid search is not implemented yet.")