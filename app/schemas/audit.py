from datetime import datetime
from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    event_id: str
    actor_id: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: str
    created_at: datetime
    details: dict = Field(default_factory=dict)


class AuditListResponse(BaseModel):
    items: list[AuditEvent] = Field(default_factory=list)
