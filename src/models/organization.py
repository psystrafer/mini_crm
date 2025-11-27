from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.organization_member import OrganizationMember


class Organization(Base):

    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    users = relationship("User", secondary=OrganizationMember, backref="Organization")
