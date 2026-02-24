from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.client import ClientRepo
from app.repo.operator import OperatorRepo


class RepoProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def get_client_repo(self, session: AsyncSession) -> ClientRepo:
        return ClientRepo(session=session)

    @provide(scope=Scope.REQUEST)
    def get_operator_repo(self, session: AsyncSession) -> OperatorRepo:
        return OperatorRepo(session=session)