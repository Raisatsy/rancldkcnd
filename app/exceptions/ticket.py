


class TicketNotFound(Exception):
    def __init__(self, id: int) -> None:
        self.id = id


class TicketInvalidStatusTransition(Exception):
    def __init__(self, old_status: str, new_status: str) -> None:
        self.old_status = old_status
        self.new_status = new_status