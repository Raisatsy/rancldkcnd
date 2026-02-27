from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticket
from app.models.enum import TicketStatus


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

    async def get_next_from_queue(self) -> Ticket | None:
        query = (
            select(Ticket)
            .where(
                Ticket.status == TicketStatus.NEW,
                Ticket.operator_id.is_(None),
            )
            .order_by(
                Ticket.priority.desc(),
                Ticket.created_at.asc(),
            )
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
