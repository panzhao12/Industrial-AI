from fastapi import APIRouter

from app.data.mock_data import list_evaluation_cases
from app.schemas.evaluation import EvaluationCase

router = APIRouter()


@router.get("/cases", response_model=list[EvaluationCase])
async def evaluation_cases() -> list[EvaluationCase]:
    return list_evaluation_cases()
