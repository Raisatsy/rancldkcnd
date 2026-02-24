from dataclasses import dataclass

from app.core.logger import logger
from app.exceptions.operator import OperatorNotFound
from app.models import Operator
from app.repo.operator import OperatorRepo
from app.schemas.base import PaginationParams, PaginatedResponse
from app.schemas.operator import OperatorCreate, OperatorRead, OperatorUpdate


@dataclass
class OperatorService:
    operator_repo: OperatorRepo

    async def create(self, operator_data: OperatorCreate) -> OperatorRead:
        logger.info(f"Create operator: {operator_data}")
        operator = Operator(**operator_data.model_dump(exclude_none=True))
        await self.operator_repo.create(operator=operator)

        await self.operator_repo.session.commit()
        operator_read = OperatorRead.model_validate(operator)
        return operator_read

    async def get_by_id(self, id: int) -> OperatorRead:
        logger.info(f"Get operator by: {id}")
        operator = await self.operator_repo.get_by_id(id=id)
        if operator is None:
            raise OperatorNotFound(id=id)

        operator_read = OperatorRead.model_validate(operator)
        return operator_read

    async def update(self, id: int, operator_data: OperatorUpdate) -> OperatorRead:
        logger.info(f"Update operator by: {id} with {operator_data}")
        operator = await self.operator_repo.get_by_id(id)
        if operator is None:
            raise OperatorNotFound(id=id)

        data_update = operator_data.model_dump(exclude_unset=True)
        operator = await self.operator_repo.update(id=id, values=data_update)
        await self.operator_repo.session.commit()

        operator_read = OperatorRead.model_validate(operator)
        return operator_read

    async def list(self, offset: int, limit: int) -> PaginatedResponse[OperatorRead]:
        logger.info(f"List operators: {offset} and {limit}")
        operators, total = await self.operator_repo.list(offset=offset, limit=limit)
        items = [OperatorRead.model_validate(o) for o in operators]
        return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)

    async def delete(self, id: int):
        logger.info(f"Delete operator: {id}")
        operator = await self.operator_repo.get_by_id(id=id)
        if operator is None:
            raise OperatorNotFound(id=id)
        await self.operator_repo.delete(operator=operator)
