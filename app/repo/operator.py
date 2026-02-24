from dataclasses import dataclass

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Operator


@dataclass
class OperatorRepo:
    session: AsyncSession

    async def create(self, operator: Operator) -> Operator:
        self.session.add(operator)
        return operator

    async def get_by_id(self, id: int) -> Operator | None:
        query = select(Operator).where(Operator.id == id)
        result = await self.session.execute(query)
        operator = result.scalar_one_or_none()
        return operator

    async def list(self, offset: int, limit: int) -> tuple[list[Operator], int]:
        total_query = select(func.count()).select_from(Operator)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar()

        query = select(Operator).order_by(Operator.id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        operators = result.scalars().all()
        return operators, total

    async def update(self, id: int, values: dict) -> Operator:
        query = (
            update(Operator)
            .where(Operator.id == id)
            .values(**values)
            .returning(Operator)
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete(self, operator: Operator) -> None:
        await self.session.delete(operator)

