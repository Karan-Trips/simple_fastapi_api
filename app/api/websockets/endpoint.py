from __future__ import annotations

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.core.security import decode_token
from app.api.websockets.manager import ConnectionManager

logger = logging.getLogger(__name__)
ws_router = APIRouter(tags=["Real-time WebSocket"])
manager = ConnectionManager()


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Authenticated WebSocket endpoint.
    Expects token query param: `ws://localhost:8000/ws?token=<JWT_TOKEN>`
    """
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        user_info = decode_token(token)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(token, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            username = user_info.get("username", "Unknown")
            await manager.broadcast(token, f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(token, websocket)
