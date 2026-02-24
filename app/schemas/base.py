from pydantic import BaseModel, Field


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    limit: int
    offset: int

class PaginationParams(BaseModel):
    limit: int
    offset: int