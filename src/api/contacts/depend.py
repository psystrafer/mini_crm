from fastapi import Query, Depends, HTTPException
from sqlalchemy import select, or_
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.api.base.depend import get_current_organization_id, get_token_data
from src.clients.db import AsyncSession
from src.models import Contact, User
from src.models.organization_member import OrganizationMember, Role


def get_contacts_query(
    search: str = None,
    owner_id: int = None,
    page: int = 1,
    page_size: int = Query(ge=1, le=100, default=10),
    organization_id: int = Depends(get_current_organization_id),
):
    q = select(Contact)
    if owner_id:
        q = (
            q.where(Contact.owner_id == owner_id)
            .where(Contact.organization_id == organization_id)
        )
    if search or search == "":
        q = q.filter(or_(
            Contact.name.like(f"%{search}%"),
            Contact.email.like(f"%{search}%"),
        ))
    q = q.limit(page_size)
    offset = (page - 1) * page_size
    q = q.offset(offset)
    return q


async def check_access(
    session: AsyncSession,
    owner_id: int = None,
    token_payload: dict = Depends(get_token_data),
    organization_id: int = Depends(get_current_organization_id),
):
    user_id = int(token_payload.get("sub"))
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Токен не действительный",
        )

    async with session.begin() as s:
        user = await s.execute(
            select(User.id, OrganizationMember.c.role)
            .where(User.id == user_id)
            .join(OrganizationMember, OrganizationMember.c.user_id == User.id)
            .where(OrganizationMember.c.organization_id == organization_id)
        )
        user_id, role = user.first()
        if (
            role in [Role.OWNER, Role.MANAGER, Role.ADMIN]
            or (role == Role.MEMBER and user_id == owner_id)
        ):
            return user_id
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Нет доступа",
            )
