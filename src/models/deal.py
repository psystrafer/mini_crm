import enum
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Enum, DECIMAL

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from .base import Base

class DealStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class DealStage(str, enum.Enum):
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED = "closed"


class DealCurrency(str, enum.Enum):
    USD = "USD"
    EUR = "EUR"


class Deal(Base):

    __tablename__ = "deal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(nullable=False)
    contact_id: Mapped[int] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[DealCurrency] = mapped_column(
        Enum(DealCurrency),
        nullable=False,
    )
    status: Mapped[DealStatus] = mapped_column(
        Enum(DealStatus),
        nullable=False,
        default=DealStatus.NEW,
    )
    stage: Mapped[DealStage] = mapped_column(
        Enum(DealStage),
        nullable=False,
        default=DealStage.QUALIFICATION,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
