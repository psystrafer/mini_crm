from fastapi import HTTPException
from sqlalchemy import select, insert
from starlette.status import HTTP_401_UNAUTHORIZED

from .dto import RegisterRequest, LoginRequest, LoginResponse
from ...clients.db import AsyncSession
from ...helper import get_password_hash, verify_password, create_token
from ...models import User, Organization
from ...models.organization_member import OrganizationMember
from ...settings import settings


async def register(request: RegisterRequest, session: AsyncSession):
    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        name=request.name,
    )
    organization = Organization(name=request.organization_name)

    async with session.begin() as s:
        s.add(organization)
        s.add(user)

    async with session.begin() as s:
        stmt = insert(OrganizationMember).values(
            user_id=user.id,
            organization_id=organization.id,
            role=request.role,
        )
        await s.execute(stmt)


async def login(request: LoginRequest, session: AsyncSession):
    async with session.begin() as s:
        user = await s.scalar(select(User).where(User.email == request.email))

        if verify_password(request.password, user.hashed_password):
            data = {"sub": str(user.id)}

            refresh_token, r_expire_at = create_token(
                data,
                settings.REFRESH_TOKEN_EXPIRE_DAYS,
            )
            access_token, a_expire_at = create_token(
                data,
                settings.ACCESS_TOKEN_EXPIRE_DAYS,
            )
            return LoginResponse(
                access_token=access_token,
                access_token_expires_at=a_expire_at,
                refresh_token=refresh_token,
                refresh_token_expire_at=r_expire_at,
            )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Неверные имя пользователя или пароль",
            )
