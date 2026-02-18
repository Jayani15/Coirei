from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class EventCreate(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    payload: Dict

class AnalyticsResponse(BaseModel):
    result: dict

class HealthResponse(BaseModel):
    status: str
