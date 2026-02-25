from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enum import TicketStatus, TicketPriority


class TicketCreate(BaseModel):
    subject: str
    client_id: int


class TicketUpdate(BaseModel):
    subject: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    operator_id: int | None = None


class TicketRead(BaseModel):
    id: int
    subject: str
    priority: TicketPriority
    status: TicketStatus
    client_id: int
    operator_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

