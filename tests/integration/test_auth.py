from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_201_CREATED

from src.models import User


async def test_register(client, session):
    body = {
        "email": "owner@example.com",
        "password": "StrongPassword123",
        "name": "Alice Owner",
        "organization_name": "Acme Inc",
    }

    response = await client.post("/auth/register", json=body)

    assert response.status_code == HTTP_201_CREATED

    async with session() as s:
        user = await s.scalar(select(User).where(User.email == body["email"]).options(joinedload(User.organizations)))
        assert user.email == body["email"]
        assert user.name == body["name"]
        organization = user.organizations[0]
        assert organization.name == body["organization_name"]

    async with session.begin() as s:
        await s.delete(user)
        await s.delete(organization)
