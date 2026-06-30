from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class MachineStatus(StrEnum):
    healthy = "healthy"
    warning = "warning"
    critical = "critical"
    offline = "offline"


class SensorStatus(StrEnum):
    normal = "normal"
    warning = "warning"
    critical = "critical"


class MaintenanceWindow(BaseModel):
    starts_at: datetime
    ends_at: datetime
    description: str


class Machine(BaseModel):
    id: str
    name: str
    asset_tag: str
    equipment_type: str
    line: str
    location: str
    status: MachineStatus
    criticality: str
    manufacturer: str
    model: str
    installed_at: datetime
    last_service_at: datetime
    next_maintenance: MaintenanceWindow
    monitored_signals: list[str] = Field(default_factory=list)


class SensorReading(BaseModel):
    name: str
    value: float
    unit: str
    status: SensorStatus
    trend: str


class TelemetrySnapshot(BaseModel):
    scenario_id: str | None = None
    machine_id: str
    scenario_label: str | None = None
    summary: str | None = None
    captured_at: datetime
    readings: list[SensorReading]


MachineSummary = Machine
MachineDetail = Machine
CurrentTelemetry = TelemetrySnapshot
