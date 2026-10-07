from __future__ import annotations

from fastapi import APIRouter
from app.api.v1.auth import auth_router
from app.api.v1.users import users_router
from app.api.v1.todos import todos_router
from app.api.v1.crypto import crypto_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(todos_router)
api_v1_router.include_router(crypto_router)

__all__ = ["api_v1_router", "auth_router", "users_router", "todos_router", "crypto_router"]
