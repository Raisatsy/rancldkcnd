import enum


class MessageSenderType(enum.StrEnum):
    OPERATOR = "operator"
    CLIENT = "client"

class OperatorStatus(enum.StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"

class TicketStatus(enum.StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(enum.IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4