import enum

from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, Enum, Integer

from .base import Base


class Role(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


OrganizationMember = Table(
    "organization_member",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("organization_id", ForeignKey("organization.id")),
    Column("user_id", ForeignKey("user.id")),
    Column("role", Enum(Role)),
    UniqueConstraint("organization_id", "user_id", name="uix_organization_member")
)
