from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.api.base.depend import get_token_data, get_current_organization_id
from src.clients.db import AsyncSession
from src.models import User
from src.models.organization_member import OrganizationMember, Role


async def check_update_access(
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
