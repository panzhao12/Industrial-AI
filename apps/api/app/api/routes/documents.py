from fastapi import APIRouter, status

from app.data.mock_data import list_documents
from app.schemas.document import Document, IngestDocumentRequest, IngestDocumentResponse

router = APIRouter()


@router.get("", response_model=list[Document])
async def documents() -> list[Document]:
    return list_documents()


@router.post(
    "/ingest",
    response_model=IngestDocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_document(payload: IngestDocumentRequest) -> IngestDocumentResponse:
    return IngestDocumentResponse(
        status="accepted",
        document_name=payload.name,
        message="Document ingestion placeholder accepted the request. No parsing or embeddings ran.",
    )
