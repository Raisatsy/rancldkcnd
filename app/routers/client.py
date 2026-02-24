from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import Response

from app.schemas.base import PaginatedResponse, PaginationParams
from app.schemas.client import ClientRead, ClientCreate, ClientUpdate
from app.services.client import ClientService
from app.utils.pagination import get_pagination_params

router = APIRouter(prefix="/clients", route_class=DishkaRoute)

@router.post("/")
async def create_client(client_create: ClientCreate, client_service: FromDishka[ClientService]) -> ClientRead:
    return await client_service.create(client_data=client_create)


@router.get("/{id}")
async def get_client_by_id(id: int, client_service: FromDishka[ClientService]) -> ClientRead:
    return await client_service.get_by_id(id=id)

@router.patch("/{id}")
async def update_client_by_id(id: int, client_data: ClientUpdate, client_service: FromDishka[ClientService]) -> ClientRead:
    return await client_service.update(id, client_data)

@router.delete("/{id}")
async def delete_client_by_id(id: int, client_service: FromDishka[ClientService]):
    await client_service.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/")
async def get_all_clients(
        client_service: FromDishka[ClientService],
        pagination_params: PaginationParams = Depends(get_pagination_params)
) -> PaginatedResponse[ClientRead]:
    return await client_service.list(offset=pagination_params.offset, limit=pagination_params.limit)
