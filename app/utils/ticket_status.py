from app.exceptions.ticket import TicketInvalidStatusTransition
from app.models.enum import TicketStatus

ALLOWED_TRANSITIONS = dict[TicketStatus, list[TicketStatus]] = {
    TicketStatus.NEW: [TicketStatus.IN_PROGRESS, TicketStatus.CLOSED],
    TicketStatus.IN_PROGRESS: [TicketStatus.WAITING, TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.WAITING: [TicketStatus.WAITING, TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.RESOLVED: [TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.CLOSED: []
}

def validate_status_transition(old: TicketStatus, new: TicketStatus):
    if new not in ALLOWED_TRANSITIONS[old]:
        raise TicketInvalidStatusTransition