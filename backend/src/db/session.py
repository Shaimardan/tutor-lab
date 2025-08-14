import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from alembic import command
from alembic.config import Config
from config import DATABASE_URL
from src.controllers.ws import ws_manager


class Database:
    __RETRY_COUNT = 30
    __RETRY_DELAY_IN_SECONDS = 20

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, future=True, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        self.__run_migrations("alembic", database_url)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for getting async session."""
        for attempt in range(self.__RETRY_COUNT):
            if await self.__check_db_connection():
                break
            await asyncio.sleep(self.__RETRY_DELAY_IN_SECONDS)
        else:
            raise RuntimeError("Failed to connect to the database after several attempts")

        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @staticmethod
    def __run_migrations(script_location: str, dsn: str) -> None:
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", script_location)
        alembic_cfg.set_main_option("sqlalchemy.url", dsn)
        command.upgrade(alembic_cfg, "head")

    async def __check_db_connection(self) -> bool:
        try:
            async with self.async_session() as session:
                result = await session.execute(select(1))
                return result.scalar() == 1
        except Exception as e:
            await ws_manager.broadcast(f"Database connection failed: {e}")
            return False


db_connections = Database(DATABASE_URL)


__all__ = ["db_connections"]
