from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base
from src.schemas.user_schemas import PortalRole, UserInDB


class User(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(64))
    disabled: Mapped[bool] = mapped_column()
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    __table_args__ = (UniqueConstraint("username", "email", name="uq_username_email"),)

    def to_read_model(self) -> UserInDB:
        return UserInDB(
            id=self.id,
            username=self.username,
            email=self.email,
            disabled=self.disabled,
            roles=[PortalRole(role_str) for role_str in self.roles],
            password=self.hashed_password,
        )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.fullname!r})"

    @property
    def is_user_admin(self) -> bool:
        return PortalRole.USER_ADMIN in self.roles


__all__ = ["User", "PortalRole"]
