from __future__ import annotations

from app.core.config import settings
from app.core.database import engine, get_db, init_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user, decode_token
from app.core.crypto import (
    encrypt_text, decrypt_text,
    encrypt_with_passphrase, decrypt_with_passphrase,
    encrypt_aes_gcm, decrypt_aes_gcm,
    generate_encryption_key, hash_sha256, hash_sha512, hmac_sha256
)

__all__ = [
    "settings",
    "engine",
    "get_db",
    "init_db",
    "hash_password",
    "verify_password",
    "create_access_token",
    "get_current_user",
    "decode_token",
    "encrypt_text",
    "decrypt_text",
    "encrypt_with_passphrase",
    "decrypt_with_passphrase",
    "encrypt_aes_gcm",
    "decrypt_aes_gcm",
    "generate_encryption_key",
    "hash_sha256",
    "hash_sha512",
    "hmac_sha256",
]
