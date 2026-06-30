from fastapi import APIRouter, Body, HTTPException, status

from app.data.mock_data import build_placeholder_diagnosis, get_incident, list_incidents
from app.schemas.diagnosis import Diagnosis
from app.schemas.incident import AnalyzeIncidentRequest, Incident

router = APIRouter()


@router.get("", response_model=list[Incident])
async def incidents() -> list[Incident]:
    return list_incidents()


@router.get("/{incident_id}", response_model=Incident)
async def incident_detail(incident_id: str) -> Incident:
    incident = get_incident(incident_id)
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' was not found.",
        )
    return incident


@router.post("/{incident_id}/analyze", response_model=Diagnosis)
async def analyze_incident(
    incident_id: str,
    payload: AnalyzeIncidentRequest | None = Body(default=None),
) -> Diagnosis:
    incident = get_incident(incident_id)
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' was not found.",
        )

    _ = payload or AnalyzeIncidentRequest()
    # TODO: Replace this typed placeholder with app.agent.graph once the manual
    # diagnosis agent is intentionally implemented.
    return build_placeholder_diagnosis(incident_id=incident.id)
