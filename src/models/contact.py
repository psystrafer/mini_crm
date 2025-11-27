from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from .base import Base


class Contact(Base):

    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
