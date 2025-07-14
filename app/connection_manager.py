
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, token: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(token, []).append(websocket)

    def disconnect(self, token: str, websocket: WebSocket):
        if token in self.connections:
            self.connections[token].remove(websocket)
            if not self.connections[token]:
                del self.connections[token]

    async def broadcast(self, token: str, message: str):
        if token in self.connections:
            for connection in self.connections[token]:
                await connection.send_text(message)
