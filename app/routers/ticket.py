from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.schemas.ticket import TicketCreate, TicketRead
from app.services.ticket import TicketService

router = APIRouter(
    prefix="/ticket",
    route_class=DishkaRoute
)

@router.post("/")
async def create_ticket(ticket_data: TicketCreate, ticket_service: FromDishka[TicketService]) -> TicketRead:
    return await ticket_service.create(ticket_data)

@router.get("/{id}")
async def get_ticket_by_id(id: int, ticket_service: FromDishka[TicketService]) -> TicketRead:
    return await ticket_service.get_by_id(id=id)
