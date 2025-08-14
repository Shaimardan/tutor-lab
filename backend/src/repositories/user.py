from src.db.models.user import User
from src.repositories.base_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
