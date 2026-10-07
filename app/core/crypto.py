from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from typing import Any, Dict, Optional, Tuple

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings


# ============================================================================
# Key Generation & Derivation
# ============================================================================

def generate_encryption_key() -> str:
    """Generate a cryptographically secure 256-bit URL-safe base64 key for Fernet / AES."""
    return Fernet.generate_key().decode("utf-8")


def derive_key_from_passphrase(passphrase: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    Derives a 256-bit encryption key from a user-supplied text passphrase using PBKDF2-HMAC-SHA256.
    Returns (urlsafe_base64_key_bytes, salt_bytes).
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    raw_key = kdf.derive(passphrase.encode("utf-8"))
    b64_key = base64.urlsafe_b64encode(raw_key)
    return b64_key, salt


# ============================================================================
# Fernet Symmetric Encryption & Decryption (AES-128-CBC + HMAC-SHA256)
# ============================================================================

def get_fernet_instance(custom_key: Optional[str] = None) -> Fernet:
    """Returns a Fernet instance using either a custom key or the configured app ENCRYPTION_KEY."""
    raw_key = custom_key or settings.ENCRYPTION_KEY
    if isinstance(raw_key, str):
        key_bytes = raw_key.encode("utf-8")
    else:
        key_bytes = raw_key
    return Fernet(key_bytes)


def encrypt_text(plaintext: str, custom_key: Optional[str] = None) -> str:
    """Encrypts a plaintext string into a secure ciphertext string."""
    fernet = get_fernet_instance(custom_key)
    encrypted_bytes = fernet.encrypt(plaintext.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_text(ciphertext: str, custom_key: Optional[str] = None) -> str:
    """Decrypts a ciphertext string back into the original plaintext."""
    fernet = get_fernet_instance(custom_key)
    try:
        decrypted_bytes = fernet.decrypt(ciphertext.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("Decryption failed: invalid ciphertext, corrupt data, or incorrect key.") from exc


def encrypt_json(data: Dict[str, Any], custom_key: Optional[str] = None) -> str:
    """Serializes a dictionary to JSON and encrypts it."""
    serialized = json.dumps(data)
    return encrypt_text(serialized, custom_key=custom_key)


def decrypt_json(ciphertext: str, custom_key: Optional[str] = None) -> Dict[str, Any]:
    """Decrypts ciphertext and deserializes the JSON string back into a dict."""
    plaintext = decrypt_text(ciphertext, custom_key=custom_key)
    return json.loads(plaintext)


# ============================================================================
# Passphrase-Based Encryption (Self-Contained Salt + Ciphertext)
# ============================================================================

def encrypt_with_passphrase(plaintext: str, passphrase: str) -> str:
    """
    Encrypts plaintext with a human-readable passphrase using PBKDF2 key derivation.
    Output format: base64(salt + ciphertext).
    """
    salt = os.urandom(16)
    key, _ = derive_key_from_passphrase(passphrase, salt=salt)
    fernet = Fernet(key)
    ciphertext_bytes = fernet.encrypt(plaintext.encode("utf-8"))
    combined = salt + ciphertext_bytes
    return base64.urlsafe_b64encode(combined).decode("utf-8")


def decrypt_with_passphrase(payload: str, passphrase: str) -> str:
    """Decrypts payload produced by encrypt_with_passphrase using the matching passphrase."""
    try:
        raw_combined = base64.urlsafe_b64decode(payload.encode("utf-8"))
        if len(raw_combined) < 17:
            raise ValueError("Invalid payload length.")
        salt = raw_combined[:16]
        ciphertext_bytes = raw_combined[16:]
        key, _ = derive_key_from_passphrase(passphrase, salt=salt)
        fernet = Fernet(key)
        return fernet.decrypt(ciphertext_bytes).decode("utf-8")
    except Exception as exc:
        raise ValueError("Decryption failed: incorrect passphrase or corrupted data.") from exc


# ============================================================================
# AES-256-GCM Authenticated Encryption (AEAD)
# ============================================================================

def encrypt_aes_gcm(plaintext: str, key_b64: Optional[str] = None, associated_data: Optional[str] = None) -> Dict[str, str]:
    """Performs AES-256-GCM AEAD encryption."""
    if key_b64:
        raw_key = base64.urlsafe_b64decode(key_b64.encode("utf-8"))
        if len(raw_key) != 32:
            raw_key = hashlib.sha256(raw_key).digest()
    else:
        raw_key = hashlib.sha256(settings.ENCRYPTION_KEY.encode("utf-8")).digest()

    aesgcm = AESGCM(raw_key)
    nonce = os.urandom(12)  # Standard 96-bit nonce for AES-GCM
    aad_bytes = associated_data.encode("utf-8") if associated_data else None

    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad_bytes)

    return {
        "algorithm": "AES-256-GCM",
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "associated_data": associated_data or "",
    }


def decrypt_aes_gcm(
    nonce_b64: str,
    ciphertext_b64: str,
    key_b64: Optional[str] = None,
    associated_data: Optional[str] = None
) -> str:
    """Decrypts AES-256-GCM ciphertext using the nonce and key."""
    try:
        if key_b64:
            raw_key = base64.urlsafe_b64decode(key_b64.encode("utf-8"))
            if len(raw_key) != 32:
                raw_key = hashlib.sha256(raw_key).digest()
        else:
            raw_key = hashlib.sha256(settings.ENCRYPTION_KEY.encode("utf-8")).digest()

        aesgcm = AESGCM(raw_key)
        nonce = base64.b64decode(nonce_b64.encode("utf-8"))
        ciphertext = base64.b64decode(ciphertext_b64.encode("utf-8"))
        aad_bytes = associated_data.encode("utf-8") if associated_data else None

        plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, aad_bytes)
        return plaintext_bytes.decode("utf-8")
    except Exception as exc:
        raise ValueError("AES-GCM decryption failed: authentication tag mismatch or invalid key.") from exc


# ============================================================================
# Cryptographic Hashing Utilities
# ============================================================================

def hash_sha256(data: str) -> str:
    """Computes standard SHA-256 hex digest."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def hash_sha512(data: str) -> str:
    """Computes standard SHA-512 hex digest."""
    return hashlib.sha512(data.encode("utf-8")).hexdigest()


def hmac_sha256(data: str, secret: Optional[str] = None) -> str:
    """Computes HMAC-SHA256 hex digest."""
    key = (secret or settings.SECRET_KEY).encode("utf-8")
    return hmac.new(key, data.encode("utf-8"), hashlib.sha256).hexdigest()
