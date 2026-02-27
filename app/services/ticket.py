from dataclasses import dataclass

from app.core.logger import logger
from app.exceptions.ticket import TicketNotFound
from app.models import Ticket
from app.models.enum import TicketStatus
from app.repo.operator import OperatorRepo
from app.repo.ticket import TicketRepo
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.utils.ticket_status import validate_status_transition


@dataclass
class TicketService:
    ticket_repo: TicketRepo
    operator_repo: OperatorRepo

    async def create(self, ticket_data: TicketCreate) -> TicketRead:
        logger.info(f"Create ticket ticket_data={ticket_data}")
        async with self.ticket_repo.session.begin():
            ticket = Ticket(subject=ticket_data.subject, client_id=ticket_data.client_id)

            operator = await self.operator_repo.get_free_operator_for_ticket()
            logger.info(f"Got free operator with id={operator.id}")

            if operator is not None:
                ticket.operator_id = operator.id
                ticket.status = TicketStatus.IN_PROGRESS
            else:
                ticket.status = TicketStatus.NEW

            await self.ticket_repo.create(ticket=ticket)

        ticket_read = TicketRead.model_validate(ticket)
        logger.info(f"Created ticket ticket_read={ticket_read}")
        return ticket_read

    async def get_by_id(self, id: int) -> TicketRead:
        logger.info(f"Get ticket id={id}")
        ticket = await self.ticket_repo.get_by_id(id=id)
        if ticket is None:
            raise TicketNotFound(id)
        ticket_read = TicketRead.model_validate(ticket)
        return ticket_read


    async def update(self, id: int, ticket_data: TicketUpdate) -> TicketRead:
        logger.info(f"Update ticket id={id} with data={ticket_data}")
        async with self.ticket_repo.session.begin():
            ticket = await self.ticket_repo.get_by_id_for_update(id=id)
            if ticket is None:
                raise TicketNotFound(id)
            old_status = ticket.status
            old_operator_id = ticket.operator_id

            if ticket_data.status is not None:
                validate_status_transition(old=ticket.status, new=ticket_data.status)
            ticket_update = ticket_data.model_dump(exclude_unset=True)
            ticket = await self.ticket_repo.update(id=id, values=ticket_update)

            if (old_operator_id is not None
            and old_status in [TicketStatus.IN_PROGRESS, TicketStatus.WAITING]
            and ticket.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]):
                next_ticket = await self.ticket_repo.get_next_from_queue()
                if next_ticket is not None:
                    logger.info(f"Get new ticket={next_ticket.id} to operator_id={old_operator_id}")
                    await self.ticket_repo.update(id=next_ticket.id, values={"operator_id": old_operator_id, "ticket_status": TicketStatus.IN_PROGRESS})

        ticket_read = TicketRead.model_validate(ticket)
        logger.info(f"Updated ticket ticket_read={ticket_read}")
        return ticket_read



