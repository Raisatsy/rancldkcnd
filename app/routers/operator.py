from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from app.schemas.base import PaginatedResponse, PaginationParams
from app.schemas.operator import OperatorCreate, OperatorRead, OperatorUpdate
from app.services.operator import OperatorService
from app.utils.pagination import get_pagination_params

router = APIRouter(prefix="/operators", route_class=DishkaRoute)

@router.post("/")
async def create_operator(operator_create: OperatorCreate, operator_service: FromDishka[OperatorService]) -> OperatorRead:
    return await operator_service.create(operator_data=operator_create)

@router.get("/{id}")
async def get_operator_by_id(id: int, operator_service: FromDishka[OperatorService]) -> OperatorRead:
    return await operator_service.get_by_id(id=id)

@router.get("/")
async def get_all_operators(operator_service: FromDishka[OperatorService],
                            pagination_param: PaginationParams = Depends(get_pagination_params)
) -> PaginatedResponse[OperatorRead]:
    return await operator_service.list(offset=pagination_param.offset, limit=pagination_param.limit)

@router.patch("/{id}")
async def update_operator_by_id(id: int, operator_update: OperatorUpdate, operator_service: FromDishka[OperatorService]):
    return await operator_service.update(id=id, operator_data=operator_update)

@router.delete("/{id}")
async def delete_operator_by_id(id: int, operator_service: FromDishka[OperatorService]):
    await operator_service.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
