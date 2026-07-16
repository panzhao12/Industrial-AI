from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from pathlib import Path

from pydantic import BaseModel, Field

from app.rag.schemas import RetrievalQuery, RetrievalResult


class RagEvalCase(BaseModel):
    id: str
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float | None = Field(default=0.8, ge=-1.0, le=1.0)
    expected_chunk_ids: list[str] = Field(default_factory=list)
    expected_document_ids: list[str] = Field(default_factory=list)
    should_return_results: bool = True


class RagEvalCaseResult(BaseModel):
    id: str
    query: str
    passed: bool
    reason: str
    returned_chunk_ids: list[str]
    returned_document_ids: list[str]
    top_score: float | None = None


class RagEvalSummary(BaseModel):
    total: int
    passed: int
    failed: int
    pass_rate: float
    results: list[RagEvalCaseResult]


RetrieveFn = Callable[[RetrievalQuery], Awaitable[RetrievalResult]]


def load_eval_cases(path: Path) -> list[RagEvalCase]:
    if not path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("Evaluation file must contain a JSON list.")

    return [RagEvalCase.model_validate(item) for item in raw]


async def evaluate_rag_cases(
    cases: list[RagEvalCase],
    retrieve: RetrieveFn,
) -> RagEvalSummary:
    results: list[RagEvalCaseResult] = []

    for case in cases:
        retrieval_result = await retrieve(
            RetrievalQuery(
                query=case.query,
                top_k=case.top_k,
            )
        )

        filtered_results = [
            item
            for item in retrieval_result.results
            if case.min_score is None or item.score >= case.min_score
        ]

        returned_chunk_ids = [item.chunk_id for item in filtered_results]
        returned_document_ids = [item.document_id for item in filtered_results]
        top_score = filtered_results[0].score if filtered_results else None

        if not case.should_return_results:
            passed = len(filtered_results) == 0
            reason = (
                "Expected no results and no results were returned."
                if passed
                else "Expected no results, but some results were returned."
            )
        else:
            expected_chunk_hit = bool(
                set(case.expected_chunk_ids).intersection(returned_chunk_ids)
            )
            expected_document_hit = bool(
                set(case.expected_document_ids).intersection(returned_document_ids)
            )

            passed = expected_chunk_hit or expected_document_hit

            if passed:
                reason = "Expected chunk or document was returned."
            else:
                reason = "Expected chunk/document was not returned."

        results.append(
            RagEvalCaseResult(
                id=case.id,
                query=case.query,
                passed=passed,
                reason=reason,
                returned_chunk_ids=returned_chunk_ids,
                returned_document_ids=returned_document_ids,
                top_score=top_score,
            )
        )

    passed_count = sum(1 for item in results if item.passed)
    failed_count = len(results) - passed_count

    return RagEvalSummary(
        total=len(results),
        passed=passed_count,
        failed=failed_count,
        pass_rate=passed_count / len(results) if results else 0.0,
        results=results,
    )