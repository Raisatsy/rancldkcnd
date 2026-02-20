import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enum import OperatorStatus




class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    status: Mapped[OperatorStatus] = mapped_column(Enum(OperatorStatus, native_enum=False), default=OperatorStatus.OFFLINE)
    is_active: Mapped[bool] = mapped_column(default=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="operator")