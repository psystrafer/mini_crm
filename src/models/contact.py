from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Contact(Base):

    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(nullable=False, default=False)
    owner_id: Mapped[int] = mapped_column(nullable=False, default=False)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
