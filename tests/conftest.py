import pytest
from httpx import ASGITransport, AsyncClient

from src.clients.db import async_engine, AsyncSessionLocal
from src.main import create_app
from src.models import Base


@pytest.fixture(scope="session")
async def app():
    return create_app()


@pytest.fixture(scope="session")
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await async_engine.dispose()
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest.fixture
async def session():
    yield AsyncSessionLocal
    await async_engine.dispose()
