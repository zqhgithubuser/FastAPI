import logging
from typing import Annotated

from fastapi import Depends, FastAPI, WebSocket, WebSocketException, status
from fastapi.websockets import WebSocketDisconnect

from app.chat import router as chat_router
from app.security import get_username_from_token

logger = logging.getLogger("uvicorn")

app = FastAPI()
app.include_router(chat_router)


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Welcome to the chat room!")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            await websocket.send_text("Message received!")
            if data == "disconnect":  # 服务端关闭连接
                logger.warn("Disconnecting...")
                await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE, reason="Disconnecting..."
                )
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION, reason="Inappropriate message"
                )
    except WebSocketDisconnect:  # 客户端断开连接
        logger.warning("Connection closed by the client")


@app.websocket("/secured-ws")
async def secure_websocket(
    websocket: WebSocket, username: Annotated[get_username_from_token, Depends()]
):
    await websocket.accept()
    await websocket.send_text(f"Welcome {username}!")
    async for data in websocket.iter_text():
        await websocket.send_text(f"You wrote: {data}")
