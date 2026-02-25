from dishka import Provider, Scope, provide

from app.repo.client import ClientRepo
from app.repo.operator import OperatorRepo
from app.repo.ticket import TicketRepo
from app.services.client import ClientService
from app.services.operator import OperatorService
from app.services.ticket import TicketService


class ServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def get_client_service(self, client_repo: ClientRepo) -> ClientService:
        return ClientService(client_repo=client_repo)

    @provide(scope=Scope.REQUEST)
    def get_operator_service(self, operator_repo: OperatorRepo) -> OperatorService:
        return OperatorService(operator_repo=operator_repo)

    @provide(scope=Scope.REQUEST)
    def get_ticket_service(self, ticket_repo: TicketRepo, operator_repo: OperatorRepo) -> TicketService:
        return TicketService(ticket_repo=ticket_repo, operator_repo=operator_repo)