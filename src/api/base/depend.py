from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi import Header
from fastapi.params import Security
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.clients.db import AsyncSession
from src.models import User
from src.models.organization_member import OrganizationMember, Role
from src.settings import settings

AccessToken = Annotated[str, Security(APIKeyHeader(name="x-access-token"))]


async def get_token_data(token: AccessToken):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Токен не действительный",
        )
    return payload


async def get_current_organization_id(
    x_organization_id: Annotated[int, Header(name="x-organization-id")]
):
    return x_organization_id


async def get_current_user(
    session: AsyncSession,
    token_payload: dict = Depends(get_token_data),
):
    user_id = int(token_payload.get("sub"))
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Токен не действительный",
        )

    async with session.begin() as s:
        user = await s.scalar(
            select(User)
            .options(joinedload(User.organizations))
            .where(User.id == user_id)
        )

        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Токен не действительный",
            )
    return user


async def check_read_access(
    session: AsyncSession,
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
        if role in [Role.OWNER, Role.MANAGER, Role.ADMIN, Role.MEMBER]:
            return user_id
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Нет доступа",
            )


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
