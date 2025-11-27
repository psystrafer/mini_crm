from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.organization_member import OrganizationMember


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str]
    name: Mapped[str] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    organizations = relationship("Organization", secondary=OrganizationMember, backref="User")
