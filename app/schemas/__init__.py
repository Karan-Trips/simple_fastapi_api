from __future__ import annotations

from app.schemas.common import BaseResponse
from app.schemas.token import Token, TokenData
from app.schemas.user import (
    UserBase, UserCreate, UserLogin, UserRead,
    UserIdRequest, UserUpdateRequest,
    as_form_user_create, as_form_user_login,
    as_form_user_id, as_form_user_update
)
from app.schemas.todo import (
    TodoCreate, TodoUpdate, TodoRead, TodoId
)
from app.schemas.crypto import (
    EncryptRequest, EncryptResponse,
    DecryptRequest, DecryptResponse,
    AESGCMEncryptRequest, AESGCMDecryptRequest,
    KeyGenerateResponse, HashRequest, HashResponse
)

__all__ = [
    "BaseResponse",
    "Token",
    "TokenData",
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserRead",
    "UserIdRequest",
    "UserUpdateRequest",
    "as_form_user_create",
    "as_form_user_login",
    "as_form_user_id",
    "as_form_user_update",
    "TodoCreate",
    "TodoUpdate",
    "TodoRead",
    "TodoId",
    "EncryptRequest",
    "EncryptResponse",
    "DecryptRequest",
    "DecryptResponse",
    "AESGCMEncryptRequest",
    "AESGCMDecryptRequest",
    "KeyGenerateResponse",
    "HashRequest",
    "HashResponse",
]
