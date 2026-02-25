from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.exceptions.client import ClientNotFound
from app.models.client import Client
from app.repo.client import ClientRepo
from app.schemas.base import PaginatedResponse
from app.schemas.client import ClientCreate, ClientUpdate, ClientRead


@dataclass
class ClientService:
    client_repo: ClientRepo

    async def create(self, client_data: ClientCreate) -> ClientRead:
        logger.info(f"Create client: {client_data}")
        client = Client(name=client_data.name, surname=client_data.surname)
        await self.client_repo.create(client=client)

        await self.client_repo.session.commit()

        client_read = ClientRead.model_validate(client)
        return client_read

    async def update(self, id: int, client_data: ClientUpdate) -> ClientRead:
        logger.info(f"Update client id={id} with {client_data}")


        data_update = client_data.model_dump(exclude_unset=True)
        client = await self.client_repo.update(id=id, values=data_update)
        if client is None:
            raise ClientNotFound(id=id)

        await self.client_repo.session.commit()

        client_read = ClientRead.model_validate(client)
        return client_read

    async def get_by_id(self, id: int) -> ClientRead:
        logger.info(f"Get client: {id}")
        client = await self.client_repo.get_by_id(id=id)
        if client is None:
            raise ClientNotFound(id=id)

        client_read = ClientRead.model_validate(client)
        return client_read

    async def list(self, offset: int, limit: int) -> PaginatedResponse[ClientRead]:
        logger.info(f"List clients: offset={offset}, limit={limit}")
        clients, total = await self.client_repo.list(offset=offset, limit=limit)
        items = [ClientRead.model_validate(c) for c in clients]
        return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)


    async def delete(self, id: int):
        logger.info(f"Delete client: {id}")
        data_delete = {"is_active": False}
        client = await self.client_repo.update(id=id, values=data_delete)
        if client is None:
            raise ClientNotFound(id=id)
        await self.client_repo.session.commit()

