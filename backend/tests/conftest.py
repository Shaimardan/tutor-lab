import asyncio
from typing import Any, AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DATABASE_URL_TEST
from main import app
from src.db.models.base import Base
from src.db.session import Database, db_connections
from src.routes.dependensies import get_uow
from src.service_layer.unit_of_work import IUnitOfWork, UnitOfWork
from tests.prepare_db.create_tables import prepare_db
from tests.prepare_db.delete_tables import delete_tables

metadata = Base.metadata


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


db_test_connections = Database(DATABASE_URL_TEST)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database() -> AsyncGenerator[None, None]:
    """Create and delete test db tables and add a test user."""
    await prepare_db()

    yield

    await delete_tables()


async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        test_engine = create_async_engine(DATABASE_URL_TEST, future=True, echo=True)
        test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)
        async with test_async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    finally:
        await test_engine.dispose()


def get_uow_test() -> IUnitOfWork:
    test_engine = create_async_engine(DATABASE_URL_TEST, future=True, echo=True)
    test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)
    return UnitOfWork(test_async_session)


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """Создает новый TestClient для FastAPI.

    TestClient использует фикстуру db_session для переопределения зависимости get_db,
    которая внедряется в маршруты.
    """
    app.dependency_overrides[db_connections.get_db] = _get_test_db
    app.dependency_overrides[get_uow] = get_uow_test
    with TestClient(app, base_url="https://testserver") as client:
        auth_user(client)
        yield client


def auth_user(client, username="johndoe", password="123"):
    response = client.post(
        "api/auth/token",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.cookies
