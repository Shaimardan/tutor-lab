from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.controllers.user.auth_controller import get_current_active_user
from src.controllers.user.user_repository import UserService
from src.db.exceptions.exceptions import DBNotFoundError
from src.db.models.user import PortalRole
from src.routes.dependensies import UOWDep
from src.schemas.user_schemas import (
    PortalRoleList,
    ShowUser,
    UpdatedUserResponse,
    UpdateUserRequest,
    UserCreateRequest,
    UserPassword,
)

user_router = APIRouter(prefix="/users", tags=["Users"])
user_router.tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    }
]


@user_router.get(
    "/",
    response_model=list[ShowUser],
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
    description="Get all users.",
)
async def get_all_users(uow: UOWDep) -> list[ShowUser]:
    list_show_user: list[ShowUser] = await UserService.get_all_users(uow)
    return list_show_user


@user_router.get(
    "/all-roles",
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
)
async def get_all_roles() -> list[str]:
    return [role.value for role in PortalRole]


@user_router.post(
    "/",
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
)
async def create_user(body: UserCreateRequest, uow: UOWDep) -> int:
    try:
        return await UserService.create_user(uow, body)
    except IntegrityError as e:
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="User with this username and email already exists.",
            )
        else:
            raise HTTPException(status_code=503, detail=f"Database error: {e}")


@user_router.delete(
    "/",
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
)
async def delete_user(user_id: int, uow: UOWDep) -> int:
    try:
        deleted_user_id = await UserService.delete_user(uow, user_id)
    except DBNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"In {e.table_name} with id {e.entity_id} not found."
        )
    return deleted_user_id


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: int,
    body: UpdateUserRequest,
    uow: UOWDep,
    current_user: ShowUser = Depends(
        get_current_active_user(required_roles=PortalRole.all_roles())
    ),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )

    if user_id != current_user.id:
        if not current_user.is_user_admin:
            raise HTTPException(status_code=403, detail="Forbidden.")

    try:
        updated_user_id = await UserService.update_user(
            uow=uow, updated_user_params=updated_user_params, user_id=user_id
        )
    except DBNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"In {e.table_name} with id {e.entity_id} not found."
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.post(
    "/{user_id}/roles",
    dependencies=[Depends(get_current_active_user(required_roles=[PortalRole.USER_ADMIN]))],
)
async def add_portal_role(user_id: int, body: PortalRoleList, uow: UOWDep) -> UpdatedUserResponse:

    try:
        updated_user_id = await UserService.add_portal_role(
            uow=uow, portal_role=body, user_id=user_id
        )
    except DBNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"In {e.table_name} with id {e.entity_id} not found."
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete(
    "/{user_id}/roles",
    dependencies=[Depends(get_current_active_user(required_roles=[PortalRole.USER_ADMIN]))],
)
async def remove_portal_role(
    user_id: int, body: PortalRoleList, uow: UOWDep
) -> UpdatedUserResponse:

    try:
        updated_user_id = await UserService.remove_portal_role(
            uow=uow, portal_role=body, user_id=user_id
        )
    except DBNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"In {e.table_name} with id {e.entity_id} not found."
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.patch("/password/{user_id}")
async def change_password(
    user_id: int,
    new_password: UserPassword,
    uow: UOWDep,
    current_user: ShowUser = Depends(
        get_current_active_user(required_roles=PortalRole.all_roles())
    ),
) -> int:

    if user_id != current_user.id:
        if not current_user.is_user_admin:
            raise HTTPException(status_code=403, detail="Forbidden.")

    try:
        return await UserService.update_user_password(
            uow=uow, new_password=new_password, user_id=user_id
        )
    except DBNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"In {e.table_name} with id {e.entity_id} not found."
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
