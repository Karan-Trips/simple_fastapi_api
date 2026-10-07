from __future__ import annotations

# Backward compatibility re-export from app.core.security
from app.core.security import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    pwd_context,
    oauth2_scheme,
    http_bearer,
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    get_current_user,
)

__all__ = [
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "pwd_context",
    "oauth2_scheme",
    "http_bearer",
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "get_current_user",
]
