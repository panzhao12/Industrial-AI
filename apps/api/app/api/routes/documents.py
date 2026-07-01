from fastapi import APIRouter, HTTPException, status

from app.data.mock_data import (
    build_placeholder_ingestion_response,
    get_document,
    list_document_chunks,
    list_documents,
)
from app.schemas.document import Document, DocumentChunk, IngestDocumentRequest, IngestDocumentResponse

router = APIRouter()


@router.get("", response_model=list[Document])
async def documents() -> list[Document]:
    return list_documents()


@router.get("/{document_id}", response_model=Document)
async def document_detail(document_id: str) -> Document:
    document = get_document(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' was not found.",
        )
    return document


@router.get("/{document_id}/chunks", response_model=list[DocumentChunk])
async def document_chunks(document_id: str) -> list[DocumentChunk]:
    document = get_document(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' was not found.",
        )
    return list_document_chunks(document_id)


@router.post(
    "/ingest",
    response_model=IngestDocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_document(payload: IngestDocumentRequest) -> IngestDocumentResponse:
    return build_placeholder_ingestion_response(payload)
