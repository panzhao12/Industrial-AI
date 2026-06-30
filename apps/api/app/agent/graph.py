from typing import Protocol

from app.agent.state import DiagnosisAgentState
from app.schemas.diagnosis import Diagnosis


class DiagnosisAgentGraph(Protocol):
    async def run(self, state: DiagnosisAgentState) -> Diagnosis:
        """Run a future diagnosis graph and return a typed diagnosis."""


class PlaceholderDiagnosisAgentGraph:
    async def run(self, state: DiagnosisAgentState) -> Diagnosis:
        raise NotImplementedError("Manual diagnosis agent graph is not implemented yet.")
