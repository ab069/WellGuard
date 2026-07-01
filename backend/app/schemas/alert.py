from datetime import datetime
from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: str
    user_id: str
    well_id: str
    title: str
    severity: str
    status: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertStatusUpdate(BaseModel):
    status: str
