from __future__ import annotations

# Backward compatibility re-export from app.core.crypto
from app.core.crypto import (
    generate_encryption_key,
    derive_key_from_passphrase,
    get_fernet_instance,
    encrypt_text,
    decrypt_text,
    encrypt_json,
    decrypt_json,
    encrypt_with_passphrase,
    decrypt_with_passphrase,
    encrypt_aes_gcm,
    decrypt_aes_gcm,
    hash_sha256,
    hash_sha512,
    hmac_sha256,
)

__all__ = [
    "generate_encryption_key",
    "derive_key_from_passphrase",
    "get_fernet_instance",
    "encrypt_text",
    "decrypt_text",
    "encrypt_json",
    "decrypt_json",
    "encrypt_with_passphrase",
    "decrypt_with_passphrase",
    "encrypt_aes_gcm",
    "decrypt_aes_gcm",
    "hash_sha256",
    "hash_sha512",
    "hmac_sha256",
]
