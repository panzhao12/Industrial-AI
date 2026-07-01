from pydantic import BaseModel, Field


class RagSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RagSearchResult(BaseModel):
    document_id: str
    document_title: str
    chunk_id: str
    chunk_index: int
    section_title: str | None = None
    content: str
    score: float
    metadata: dict[str, str] = Field(default_factory=dict)
    is_placeholder: bool = True


class RagSearchResponse(BaseModel):
    query: str
    top_k: int
    results: list[RagSearchResult] = Field(default_factory=list)
    message: str
    is_placeholder: bool = True
