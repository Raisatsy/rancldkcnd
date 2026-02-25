from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticket


@dataclass
class TicketRepo:
    session: AsyncSession

    async def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        return ticket

    async def get_by_id(self, id: int) -> Ticket | None:
        query = select(Ticket).where(Ticket.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_for_update(self, id: int) -> Ticket | None:
        query = select(Ticket).where(Ticket.id == id).with_for_update()
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, id: int, values: dict) -> Ticket:
        query = (
            update(Ticket)
            .where(Ticket.id == id)
            .values(**values)
            .returning(Ticket)
            .execution_options(synchronize_session='fetch')
        )
        result = await self.session.execute(query)
        return result.scalar_one()
