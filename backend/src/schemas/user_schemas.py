from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator


class PortalRole(str, Enum):
    USER_ADMIN = "USER_ADMIN"
    TUTOR = "TUTOR"
    STUDENT = "STUDENT"

    @classmethod
    def all_roles(cls) -> list[str]:
        return [role.value for role in cls]


class ShowUser(BaseModel):
    id: int
    username: str
    email: str | None = None
    fullname: str | None = None
    disabled: bool | None = None
    roles: list[PortalRole]

    @property
    def is_user_admin(self) -> bool:
        return PortalRole.USER_ADMIN in self.roles

    @property
    def is_preset_admin(self) -> bool:
        return PortalRole.PRESET_ADMIN in self.roles

    @property
    def is_preset_editor(self) -> bool:
        return PortalRole.PRESET_EDITOR in self.roles

    @property
    def is_preset_reader(self) -> bool:
        return PortalRole.PRESET_READER in self.roles


class UserPassword(BaseModel):
    password: str


class UserInDB(ShowUser, UserPassword):
    pass


class UserCreateRequest(UserPassword):
    username: str
    email: str | None = None
    fullname: str | None = None
    disabled: bool | None = None


class UpdateUserRequest(BaseModel):
    fullname: str | None
    username: str | None
    email: EmailStr | None = None

    @field_validator("fullname", "username")
    def check_non_empty(cls, v: str | None) -> str | None:
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Field cannot be empty or only contain whitespace")
        return v


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class PortalRoleList(BaseModel):
    roles: list[PortalRole]
