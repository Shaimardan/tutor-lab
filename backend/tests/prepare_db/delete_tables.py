import asyncio

from config import DATABASE_URL_TEST
from src.db.models.base import Base
from src.db.session import Database


async def delete_tables():
    metadata = Base.metadata
    db_test_connections = Database(DATABASE_URL_TEST)
    metadata.bind = db_test_connections.engine

    async with db_test_connections.engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


if __name__ == "__main__":
    asyncio.run(delete_tables())
