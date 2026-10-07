from __future__ import annotations

# Backward compatibility adapter
from fastapi import APIRouter
from app.api.v1.auth import auth_router
from app.api.v1.users import users_router

# Combine auth and users into user_router to match legacy interface
user_router = APIRouter()
user_router.include_router(auth_router)
user_router.include_router(users_router)

__all__ = ["user_router"]
