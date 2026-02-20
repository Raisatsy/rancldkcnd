from datetime import datetime
import enum
from sqlalchemy import ForeignKey, String, func, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enum import MessageSenderType





class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    sender: Mapped[MessageSenderType] = mapped_column(Enum(MessageSenderType, native_enum=False))
    text: Mapped[str] = mapped_column(String(5000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"))
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id"))

    ticket: Mapped["Ticket"] = relationship(back_populates="messages")
    operator: Mapped["Operator"] = relationship()
    client: Mapped["Client"] = relationship()