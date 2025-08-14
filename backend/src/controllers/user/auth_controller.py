from datetime import datetime, timedelta, timezone
from typing import Annotated, Callable, Dict, List, Optional

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from jwt import PyJWTError
from starlette.websockets import WebSocket, WebSocketDisconnect

from config import auth_config
from src.controllers.user.user_repository import UserService
from src.routes.dependensies import UOWDep
from src.schemas.user_schemas import ShowUser, UserInDB
from src.service_layer.hasher import Hasher
from src.service_layer.unit_of_work import IUnitOfWork


def get_token(request: Request) -> str:
    token = request.cookies.get(auth_controller.COOKIES_TOKEN_KEY)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


def get_token_from_websocket(websocket: WebSocket) -> str:
    token = websocket.cookies.get(auth_controller.COOKIES_TOKEN_KEY)
    if not token:
        websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token not found")
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
    return token


class AuthController:
    COOKIES_TOKEN_KEY = "access_token"
    JWF_LIFE_TIME_minutes = 24 * 60

    async def login(
        self, uow: IUnitOfWork, username: str, password: str, response: Response
    ) -> Optional[Dict[str, str]]:
        """Authenticates the user with the given username and password.

        Args:
            uow (IUnitOfWork): The unit of work instance for database operations.
            username (str): The username of the user.
            password (str): The password of the user.
            response (Response): The HTTP response object for setting cookies.

        Returns:
            Optional[Dict[str, str]]: The access token if login is successful, None otherwise.
        """
        async with uow:
            user_model: UserInDB = await uow.user.find_one(username=username, disabled=False)

        if not Hasher.verify_password(Hasher.get_password_hash(password), user_model.password):
            return None

        access_token = self.__create_access_token({"username": user_model.username})

        response.set_cookie(
            key=self.COOKIES_TOKEN_KEY,
            value=access_token,
            httponly=True,
        )

        return {"access_token": access_token}

    async def logout(self, response: Response) -> None:
        """Logs out the user by deleting the access token cookie.

        Args:
            response (Response): The HTTP response object for deleting cookies.
        """
        response.delete_cookie(key=self.COOKIES_TOKEN_KEY)

    def __create_access_token(self, data: dict) -> str:
        """Creates a JWT access token.

        Args:
            data (dict): The data to include in the token payload.

        Returns:
            str: The encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc).replace(hour=0) + timedelta(
            minutes=self.JWF_LIFE_TIME_minutes
        )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode,
            auth_config.VERIFYING_KEY.get_secret_value(),
            algorithm=auth_config.JWT_ALGORITHM,
        )
        return encode_jwt

    @classmethod
    async def __decode_token(cls, token: str, uow: IUnitOfWork) -> ShowUser:
        """Decodes and verifies a JWT token.

        Args:
            token (str): The JWT token.
            uow (IUnitOfWork): The unit of work instance for database operations.

        Returns:
            ShowUser: The user associated with the token.

        Raises:
            HTTPException: If the token is invalid, expired, or the user is not found.
        """
        try:
            payload = jwt.decode(
                token,
                auth_config.VERIFYING_KEY.get_secret_value(),
                algorithms=auth_config.JWT_ALGORITHM,
            )
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        expire = payload.get("exp")
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired"
            )

        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="The user was not found"
            )

        user: ShowUser = await UserService.get_user_by_username(uow, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user

    async def get_current_user(
        self,
        uow: UOWDep,
        token: str = Depends(get_token),
    ) -> ShowUser:
        """Retrieves the current authenticated user using a token.

        Args:
            uow (UOWDep): The unit of work dependency for database operations.
            token (str, optional): The JWT token, provided by dependency injection.

        Returns:
            ShowUser: The authenticated user.

        Raises:
            HTTPException: If the token is not provided.
        """
        if not token or token.lower() == "null":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not provided",
            )

        user: ShowUser = await self.__decode_token(token, uow)

        return user

    async def get_current_user_from_websocket(
        self, uow: UOWDep, token: str = Depends(get_token_from_websocket)
    ) -> ShowUser:
        """Retrieves the current authenticated user for a WebSocket connection.

        Args:
            uow (UOWDep): The unit of work dependency for database operations.
            token (str, optional): The JWT token, provided by dependency injection for WebSockets.

        Returns:
            ShowUser: The authenticated user.

        Raises:
            HTTPException: If the token is not provided.
        """
        if not token or token.lower() == "null":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not provided",
            )

        user = await self.__decode_token(token, uow)

        return user


auth_controller = AuthController()


async def _check_active_user_roles(current_user: ShowUser, required_roles: List[str]) -> ShowUser:
    """Checks if the user is active and has the required roles.

    Args:
        current_user (ShowUser): The current user.
        required_roles (List[str]): List of required roles.

    Returns:
        ShowUser: The current user if they are active and have the necessary roles.

    Raises:
        HTTPException: If the user is inactive or lacks the required roles.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    user_roles = [role for role in current_user.roles]
    if not any(role in user_roles for role in required_roles):
        raise HTTPException(status_code=403, detail="Insufficient roles")

    return current_user


def get_current_active_user(required_roles: List[str]) -> Callable:
    """Returns a function to retrieve the current active user with role checking (for HTTP).

    Args:
        required_roles (List[str]): List of required roles.

    Returns:
        Callable: A function to get the current active user.
    """

    async def _get_current_active_user(
        current_user: Annotated[ShowUser, Depends(auth_controller.get_current_user)],
    ) -> ShowUser:
        return await _check_active_user_roles(current_user, required_roles)

    return _get_current_active_user


def get_current_active_user_from_websocket(required_roles: List[str]) -> Callable:
    """Returns a function to retrieve the current active user with role checking (for WebSocket).

    Args:
        required_roles (List[str]): List of required roles.

    Returns:
        Callable: A function to get the current active user.
    """

    async def _get_current_active_user(
        current_user: Annotated[ShowUser, Depends(auth_controller.get_current_user_from_websocket)],
    ) -> ShowUser:
        return await _check_active_user_roles(current_user, required_roles)

    return _get_current_active_user
