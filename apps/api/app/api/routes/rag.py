from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.rag.runtime import clear_rag_index, get_rag_status, ingest_local_manuals, search
from app.rag.schemas import RetrievalQuery
from app.schemas.rag import RagSearchRequest, RagSearchResponse, RagSearchResult

router = APIRouter()


def _manuals_path() -> Path:
    return Path(__file__).resolve().parents[5] / "data" / "synthetic" / "manuals"


@router.get("/status")
async def rag_status() -> dict[str, int | str]:
    return get_rag_status()


@router.post("/clear")
async def rag_clear() -> dict[str, int]:
    return clear_rag_index()


@router.post("/ingest-local-manuals")
async def rag_ingest_local_manuals() -> dict[str, int]:
    manuals_path = _manuals_path()

    if not manuals_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Manuals folder not found: {manuals_path}",
        )

    try:
        return await ingest_local_manuals(manuals_path)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/search", response_model=RagSearchResponse)
async def rag_search(payload: RagSearchRequest) -> RagSearchResponse:
    try:
        retrieval_result = await search(
            RetrievalQuery(
                query=payload.query,
                top_k=payload.top_k,
            )
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    filtered_results = [
        item
        for item in retrieval_result.results
        if payload.min_score is None or item.score >= payload.min_score
    ]

    status = get_rag_status()

    return RagSearchResponse(
        query=retrieval_result.query,
        top_k=payload.top_k,
        results=[
            RagSearchResult(
                document_id=item.document_id,
                document_title=item.document_title,
                chunk_id=item.chunk_id,
                chunk_index=item.metadata.get("chunk_index"),
                section_title=item.section_title,
                content=item.content,
                score=item.score,
                metadata=item.metadata,
                is_placeholder=False,
            )
            for item in filtered_results
        ],
        message=(
            f"RAG search completed with {status['embedding_provider']} "
            f"using {status.get('embedding_model', 'unknown model')}. "
            f"Returned {len(filtered_results)} results after min_score filtering."
        ),
        is_placeholder=False,
    )