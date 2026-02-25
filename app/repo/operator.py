from dataclasses import dataclass

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Operator, Ticket
from app.models.enum import TicketStatus, OperatorStatus


@dataclass
class OperatorRepo:
    session: AsyncSession

    async def create(self, operator: Operator) -> Operator:
        self.session.add(operator)
        return operator

    async def get_by_id(self, id: int) -> Operator | None:
        query = select(Operator).where(Operator.id == id, Operator.is_active == True)
        result = await self.session.execute(query)
        operator = result.scalar_one_or_none()
        return operator

    async def list(self, offset: int, limit: int) -> tuple[list[Operator], int]:
        total_query = select(func.count()).where(Operator.is_active == True).select_from(Operator)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar()

        query = select(Operator).where(Operator.is_active == True).order_by(Operator.id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        operators = result.scalars().all()
        return operators, total

    async def update(self, id: int, values: dict) -> Operator | None:
        query = (
            update(Operator)
            .where(Operator.id == id, Operator.is_active == True)
            .values(**values)
            .returning(Operator)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, operator: Operator) -> None:
        await self.session.delete(operator)

    async def get_free_operator_for_ticket(self) -> Operator | None:
        active_status = [
            TicketStatus.NEW,
            TicketStatus.IN_PROGRESS,
            TicketStatus.WAITING
        ]

        tickets_count_subq = (
            select(
                Ticket.operator_id,
                func.count(Ticket.operator_id).label("active_tickets")
            )
            .where(Ticket.status.in_(active_status))
            .group_by(Ticket.operator_id)
            .subquery()
        )

        query = (
            select(Operator)
            .outerjoin(
                tickets_count_subq,
                tickets_count_subq.c.operator_id == Operator.id
            )
            .where(
                Operator.is_active == True,
                Operator.status == OperatorStatus.ONLINE
            )
            .order_by(
                func.coalesce(tickets_count_subq.c.active_tickets, 0).asc(),
                Operator.id.asc()
            )
            .limit(1)
            .with_for_update(of=Operator, skip_locked=True)
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

