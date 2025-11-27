from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.organization_member import OrganizationMember


class Organization(Base):

    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    users = relationship("User", secondary=OrganizationMember, backref="Organization")
