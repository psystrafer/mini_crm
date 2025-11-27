from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Deal(Base):

    __tablename__ = "deal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(nullable=False, default=False)
    contact_id: Mapped[int] = mapped_column(nullable=False, default=False)
    owner_id: Mapped[int] = mapped_column(nullable=False, default=False)
    name: Mapped[str]
    title: Mapped[str]
    amount: Mapped[Decimal]
    currency: Mapped[str]
    status: Mapped[str]
    stage: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime]
