from typing import Any, Dict

from src.schemas import PortalRoleList, ShowUser, UserCreateRequest
from src.schemas.user_schemas import UserInDB, UserPassword
from src.service_layer.hasher import Hasher
from src.service_layer.unit_of_work import IUnitOfWork


class UserService:
    @classmethod
    async def get_all_users(cls, uow: IUnitOfWork) -> list[ShowUser]:
        async with uow:
            users: list[UserInDB] = await uow.user.find_all()
            return [
                ShowUser(
                    id=user.id,
                    username=user.username,
                    fullname=user.fullname,
                    email=user.email,
                    disabled=user.disabled,
                    roles=user.roles,
                )
                for user in users
            ]

    @classmethod
    async def create_user(cls, uow: IUnitOfWork, body: UserCreateRequest) -> int:
        async with uow:
            user_id = await uow.user.add_one(
                username=body.username,
                fullname=body.fullname,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
                disabled=body.disabled,
                roles=[],
            )
            await uow.commit()
        return user_id

    @classmethod
    async def delete_user(cls, uow: IUnitOfWork, user_id: int) -> int:
        async with uow:
            deleted_user_id = await uow.user.edit_one(row_id=user_id, data={"disabled": True})
            await uow.commit()
        return deleted_user_id

    @classmethod
    async def get_user_by_username(cls, uow: IUnitOfWork, username: str) -> ShowUser:
        async with uow:
            user: UserInDB = await uow.user.find_one(username=username)
        return ShowUser(
            id=user.id,
            username=user.username,
            fullname=user.fullname,
            email=user.email,
            disabled=user.disabled,
            roles=user.roles,
        )

    @classmethod
    async def update_user(
        cls,
        uow: IUnitOfWork,
        user_id: int,
        updated_user_params: Dict[str, Any],
    ) -> int:
        async with uow:
            updated_user_id = await uow.user.edit_one(row_id=user_id, data=updated_user_params)
            await uow.commit()
        return updated_user_id

    @classmethod
    async def add_portal_role(
        cls, uow: IUnitOfWork, user_id: int, portal_role: PortalRoleList
    ) -> int:
        async with uow:
            user_in_db: UserInDB = await uow.user.find_one(id=user_id)
            merged_roles = list(set(portal_role.roles).union(set(user_in_db.roles)))

            updated_user_id = await uow.user.edit_one(row_id=user_id, data={"roles": merged_roles})
            await uow.commit()
        return updated_user_id

    @classmethod
    async def remove_portal_role(
        cls, uow: IUnitOfWork, user_id: int, portal_role: PortalRoleList
    ) -> int:
        async with uow:
            user_in_db: UserInDB = await uow.user.find_one(id=user_id)

            user_role = set(user_in_db.roles)
            portal_role = set(portal_role.roles)
            merged_roles = list(user_role.difference(portal_role))

            updated_user_id = await uow.user.edit_one(row_id=user_id, data={"roles": merged_roles})
            await uow.commit()
        return updated_user_id

    @classmethod
    async def update_user_password(
        cls, uow: IUnitOfWork, user_id: int, new_password: UserPassword
    ) -> int:
        password_in_db = Hasher.get_password_hash(new_password.password)
        async with uow:
            updated_user_id: int = await uow.user.edit_one(
                row_id=user_id, data={"hashed_password": password_in_db}
            )
            await uow.commit()

        return updated_user_id
