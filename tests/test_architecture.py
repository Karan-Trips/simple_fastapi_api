from __future__ import annotations

import pytest


def test_clean_architecture_imports():
    """Verify clean modular architecture imports."""
    from app.core import settings, engine, get_db, init_db, hash_password, verify_password, encrypt_text, decrypt_text
    from app.models import User, Todo, SQLModel
    from app.schemas import (
        BaseResponse, Token, UserCreate, UserLogin, UserRead,
        TodoCreate, TodoUpdate, TodoRead,
        EncryptRequest, DecryptRequest, HashRequest
    )
    from app.services import UserService, TodoService, CryptoService
    from app.api.v1 import api_v1_router, auth_router, users_router, todos_router, crypto_router
    from app.api.websockets import ws_router, ConnectionManager
    from app.admin import UserAdmin, TodoAdmin, setup_admin
    from app.utils.response import create_success_response, create_error_response

    assert settings.PROJECT_NAME is not None
    assert callable(get_db)
    assert callable(hash_password)
    assert callable(encrypt_text)
    assert User.__tablename__ == "users"
    assert Todo.__tablename__ == "todos"
    assert hasattr(UserService, "get_all_users")
    assert hasattr(TodoService, "create_todo")
    assert hasattr(CryptoService, "generate_key")


def test_backward_compatibility_adapters():
    """Verify legacy import paths still work without breaking existing scripts."""
    from app import database, models, schemas
    from app.auth import get_current_user, create_access_token
    from app.auth_token_genration import get_current_user as legacy_get_user
    from app.crypto import encrypt_text, decrypt_text
    from app.response import create_success_response
    from app.repositories import user_repo, todo_repo
    from app.router import user_api, todo_api, crypto_api
    from app.connection_manager import ConnectionManager

    assert hasattr(database, "get_db")
    assert hasattr(models, "User")
    assert hasattr(schemas, "UserCreate")
    assert callable(legacy_get_user)
    assert callable(encrypt_text)
    assert callable(create_success_response)
    assert hasattr(user_repo, "get_all_users")
    assert hasattr(todo_repo, "create_todo")
    assert hasattr(user_api, "user_router")
    assert hasattr(todo_api, "todo_router")
    assert hasattr(crypto_api, "crypto_router")
    assert ConnectionManager is not None
