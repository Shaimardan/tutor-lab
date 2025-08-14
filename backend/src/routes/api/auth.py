from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.controllers.user.auth_controller import auth_controller, get_current_active_user
from src.db.exceptions.exceptions import DBNotFoundError
from src.db.models.user import PortalRole
from src.routes.dependensies import UOWDep
from src.schemas import ShowUser

auth_router = APIRouter(prefix="/auth", tags=["Authorization"])
auth_router.tags_metadata = [
    {
        "name": "Authorization",
        "description": "User authorization endpoints.",
    }
]


@auth_router.post("/token", description="User authorization and token receipt.")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, uow: UOWDep
) -> dict[str, str] | None:
    """Authenticates a user using a username and password.

     Stores the token in cookies, and performs a token and user validity check.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        response (Response): The response object for setting cookies.
        uow (UOWDep): Unit of Work dependency for handling database operations.

    Returns:
        dict[str, str] | None: The user token if authentication is successful, else None.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    try:
        user_token: dict[str, str] | None = await auth_controller.login(
            uow=uow, username=form_data.username, password=form_data.password, response=response
        )
    except DBNotFoundError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user_token


@auth_router.post(
    "/logout",
    dependencies=[Depends(get_current_active_user(required_roles=PortalRole.all_roles()))],
)
async def logout(response: Response) -> None:
    await auth_controller.logout(response=response)


@auth_router.get("/users/me", response_model=ShowUser)
async def read_users_me(
    current_user: ShowUser = Depends(
        get_current_active_user(required_roles=PortalRole.all_roles())
    ),
) -> ShowUser:
    """Retrieves the current active user's information.

    This endpoint allows authenticated users to fetch their own user details.

    Args:
        current_user (ShowUser): The current active user, resolved via dependency injection.

    Returns:
        ShowUser: The details of the current active user.

    Raises:
        HTTPException: If the user is inactive.
    """
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
