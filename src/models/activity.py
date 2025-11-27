from datetime import datetime
from typing import Dict, Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Activity(Base):

    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deal_id: Mapped[int] = mapped_column(nullable=False, default=False)
    author_id: Mapped[int] = mapped_column(nullable=True, default=None)
    type: Mapped[str]
    payload: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
