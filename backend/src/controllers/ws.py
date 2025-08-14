from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int) -> None:
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: int, message: str) -> None:
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections.values():
            await connection.send_text(message)


ws_manager = ConnectionManager()

__all__ = [
    "ws_manager",
]
