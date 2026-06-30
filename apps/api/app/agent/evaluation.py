from typing import Protocol

from app.schemas.diagnosis import Diagnosis
from app.schemas.evaluation import EvaluationCase


class EvaluationResultPlaceholder(Exception):
    """Raised until manual evaluation logic is implemented."""


class DiagnosisEvaluator(Protocol):
    async def evaluate(self, case: EvaluationCase, diagnosis: Diagnosis) -> None:
        """Evaluate a future diagnosis result against a case."""


class PlaceholderDiagnosisEvaluator:
    async def evaluate(self, case: EvaluationCase, diagnosis: Diagnosis) -> None:
        raise EvaluationResultPlaceholder("Manual diagnosis evaluation is not implemented yet.")
