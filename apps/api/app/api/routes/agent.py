from fastapi import APIRouter

from app.data.mock_data import get_agent_trace
from app.schemas.agent_trace import AgentTrace

router = APIRouter()


@router.get("/traces/{trace_id}", response_model=AgentTrace)
async def agent_trace(trace_id: str) -> AgentTrace:
    return get_agent_trace(trace_id)
