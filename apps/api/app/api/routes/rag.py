from fastapi import APIRouter

from app.data.mock_data import search_placeholder_chunks
from app.schemas.rag import RagSearchRequest, RagSearchResponse

router = APIRouter()


@router.post("/search", response_model=RagSearchResponse)
async def rag_search(payload: RagSearchRequest) -> RagSearchResponse:
    return RagSearchResponse(
        query=payload.query,
        top_k=payload.top_k,
        results=search_placeholder_chunks(query=payload.query, top_k=payload.top_k),
        message=(
            "Placeholder RAG search only. No embeddings, vector similarity, hybrid search, "
            "LLM reranking, or diagnosis generation ran."
        ),
        is_placeholder=True,
    )
