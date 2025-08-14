from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.repositories.user import UserRepository


class IUnitOfWork(ABC):
    """Interface for Unit of Work pattern. Manages repositories and transactional behavior."""
    user: UserRepository

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> None:
        pass

    @abstractmethod
    async def __aexit__(self, *args: Any) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.user = UserRepository(self.session)

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
