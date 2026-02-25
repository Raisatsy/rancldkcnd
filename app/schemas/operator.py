from pydantic import BaseModel, ConfigDict

from app.models.enum import OperatorStatus


class OperatorCreate(BaseModel):
    name: str
    surname: str

class OperatorUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    status: OperatorStatus | None = None

class OperatorRead(BaseModel):
    id: int
    name: str
    surname: str
    status: OperatorStatus
    is_active: bool

    model_config = ConfigDict(from_attributes=True)