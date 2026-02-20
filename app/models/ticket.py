import enum
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    Enum,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enum import TicketStatus, TicketPriority




class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(255))
    priority: Mapped[TicketPriority] = mapped_column(Integer, default=TicketPriority.LOW)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, native_enum=False), default=TicketStatus.NEW)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    operator: Mapped["Operator"] = relationship(back_populates="tickets")
    client: Mapped["Client"] = relationship(back_populates="tickets")
    messages: Mapped[list["Message"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    status_history: Mapped[list["TicketStatusHistory"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")


class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    old_status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, native_enum=False))
    new_status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, native_enum=True))
    change_by: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ticket: Mapped["Ticket"] = relationship(back_populates="status_history")
    operator: Mapped["Operator"] = relationship()