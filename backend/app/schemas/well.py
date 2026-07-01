from datetime import datetime
from pydantic import BaseModel


class WellCreate(BaseModel):
    well_name: str
    well_type: str
    depth: float = 0.0
    pressure: float = 0.0
    temperature: float = 0.0
    flow_rate: float = 0.0


class WellResponse(BaseModel):
    id: str
    user_id: str
    well_name: str
    well_type: str
    status: str
    depth: float
    pressure: float
    temperature: float
    flow_rate: float
    integrity_score: int
    last_inspected: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
