from dataclasses import dataclass

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client


@dataclass
class ClientRepo:
    session: AsyncSession

    async def create(self, client: Client) -> Client:
        self.session.add(client)
        return client

    async def get_by_id(self, id: int) -> Client | None:
        query = select(Client).where(Client.id == id, Client.is_active == True)
        result = await self.session.execute(query)
        client = result.scalar_one_or_none()
        return client

    async def list(self, offset: int, limit: int) -> tuple[list[Client], int]:
        total_query = select(func.count()).where(Client.is_active == True).select_from(Client)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar_one()

        query = select(Client).where(Client.is_active == True).order_by(Client.id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        clients = result.scalars().all()
        return clients, total

    async def update(self, id: int, values: dict) -> Client | None:
        query = (
            update(Client)
            .where(Client.id == id, Client.is_active == True)
            .values(**values)
            .returning(Client)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, client: Client) -> None:
        await self.session.delete(client)