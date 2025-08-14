from typing import Any

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.controllers.ws import ws_manager

from ...controllers.user.auth_controller import get_current_active_user_from_websocket
from ...db.models.user import PortalRole
from ...schemas import ShowUser
from .auth import auth_router
from .localization import localization_router
from .user import user_router


def collect_openapi_tags(*all_routers: APIRouter) -> list[dict[str, Any]]:
    tags = []
    for arg in all_routers:
        if hasattr(arg, "tags_metadata"):
            tags.extend(arg.tags_metadata)
    return tags


api_router = APIRouter(
    prefix="/api",
)


@api_router.get("/ping")
def ping() -> str:
    return "pong"


routers = [
    auth_router,
    user_router,
    localization_router,
]

for router in routers:
    api_router.include_router(router)
tags_metadata = collect_openapi_tags(*routers)


@api_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: ShowUser = Depends(
        get_current_active_user_from_websocket(required_roles=PortalRole.all_roles())
    ),
) -> None:
    await ws_manager.connect(current_user.id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_personal_message(f"WS Pong: {data}", websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(current_user.id)


__all__ = [
    "api_router",
]
