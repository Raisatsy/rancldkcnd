from fastapi import Query

from app.schemas.base import PaginationParams


def get_pagination_params(limit: int = Query(default=50, ge=1, le=500), offset: int = Query(default=0, ge=0)) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)