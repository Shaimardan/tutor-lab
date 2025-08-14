import asyncio

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from config import DATABASE_URL_TEST
from src.db.models.base import Base
from src.db.models.user import PortalRole, User
from src.db.session import Database


async def prepare_db():
    metadata = Base.metadata
    db_test_connections = Database(DATABASE_URL_TEST)
    metadata.bind = db_test_connections.engine

    async with db_test_connections.engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    async with AsyncSession(db_test_connections.engine) as session:
        test_user = {
            "username": "johndoe",
            "fullname": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
            "disabled": False,
            "roles": [role.value for role in PortalRole],
        }

        test_user_without_role = {
            "username": "johndoe_without_role",
            "fullname": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
            "disabled": False,
            "roles": [],
        }

        await session.execute(insert(User).values(test_user))
        await session.execute(insert(User).values(test_user_without_role))

        for role in PortalRole:
            test_user_with_role = {
                "username": f"johndoe{role.value}",
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "disabled": False,
                "roles": [role.value],
            }
            await session.execute(insert(User).values(test_user_with_role))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(prepare_db())
