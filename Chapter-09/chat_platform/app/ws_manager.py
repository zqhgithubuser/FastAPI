import asyncio

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    async def broadcast(self, message: dict, exclude: WebSocket = None):
        tasks = []
        for connection in self.active_connections:
            if connection != exclude:
                tasks.append(self._send_message_safe(connection, message))
        await asyncio.gather(*tasks)

    async def _send_message_safe(self, connection: WebSocket, message: dict):
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            self.disconnect(connection)
