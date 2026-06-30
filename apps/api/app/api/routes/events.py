import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


async def diagnosis_events(incident_id: str) -> AsyncIterator[str]:
    payload = {
        "incident_id": incident_id,
        "status": "placeholder",
        "message": "Realtime diagnosis updates are not implemented yet.",
        "emitted_at": datetime.now(UTC).isoformat(),
    }
    yield f"event: diagnosis_status\ndata: {json.dumps(payload)}\n\n"


@router.get("/diagnosis/{incident_id}")
async def diagnosis_event_stream(incident_id: str) -> StreamingResponse:
    return StreamingResponse(
        diagnosis_events(incident_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
