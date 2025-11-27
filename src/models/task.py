from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deal_id: Mapped[int] = mapped_column(nullable=False, default=False)
    title: Mapped[str]
    description: Mapped[str]
    due_date: Mapped[datetime]
    is_done: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
