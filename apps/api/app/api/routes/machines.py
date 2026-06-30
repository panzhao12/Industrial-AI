from fastapi import APIRouter, HTTPException, status

from app.data.mock_data import get_current_telemetry, get_machine, list_machines
from app.schemas.machine import Machine, TelemetrySnapshot

router = APIRouter()


@router.get("", response_model=list[Machine])
async def machines() -> list[Machine]:
    return list_machines()


@router.get("/{machine_id}", response_model=Machine)
async def machine_detail(machine_id: str) -> Machine:
    machine = get_machine(machine_id)
    if machine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Machine '{machine_id}' was not found.",
        )
    return machine


@router.get("/{machine_id}/telemetry/current", response_model=TelemetrySnapshot)
async def machine_current_telemetry(machine_id: str) -> TelemetrySnapshot:
    telemetry = get_current_telemetry(machine_id)
    if telemetry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Telemetry for machine '{machine_id}' was not found.",
        )
    return telemetry
