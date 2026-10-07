from __future__ import annotations

from app.api.v1 import api_v1_router, auth_router, users_router, todos_router, crypto_router
from app.api.websockets import ws_router, ConnectionManager

__all__ = [
    "api_v1_router",
    "auth_router",
    "users_router",
    "todos_router",
    "crypto_router",
    "ws_router",
    "ConnectionManager"
]
