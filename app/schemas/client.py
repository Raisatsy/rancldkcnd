from pydantic import BaseModel, ConfigDict


class ClientCreate(BaseModel):
    name: str
    surname: str

class ClientUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None


class ClientRead(BaseModel):
    id: int
    name: str
    surname: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)