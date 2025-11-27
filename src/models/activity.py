import enum
from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ActivityType(str, enum.Enum):
    COMMENT = "comment"
    STATUS_CHANGED = "status_changed"
    TASK_CREATED = "task_created"
    SYSTEM = "system"


class Activity(Base):

    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deal_id: Mapped[int] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(nullable=True, default=None)
    type: Mapped[ActivityType] = mapped_column(Enum(ActivityType), nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    created_at = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
