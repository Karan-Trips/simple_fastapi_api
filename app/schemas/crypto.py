from __future__ import annotations

from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class EncryptRequest(SQLModel):
    text: str = Field(..., description="Plaintext to encrypt", examples=["Secret database credentials or confidential text"])
    key: Optional[str] = Field(None, description="Optional custom 256-bit Fernet key (leave null to use server key)")
    passphrase: Optional[str] = Field(None, description="Optional passphrase for PBKDF2 key derivation", examples=["MySecurePassphrase!2026"])


class EncryptResponse(SQLModel):
    ciphertext: str = Field(..., description="Encrypted ciphertext string")
    algorithm: str = Field(default="AES-256 (Fernet / CBC + HMAC)", description="Encryption algorithm used")
    method: str = Field(..., description="Method used: server_key, custom_key, or passphrase")


class DecryptRequest(SQLModel):
    ciphertext: str = Field(..., description="Ciphertext to decrypt")
    key: Optional[str] = Field(None, description="Custom 256-bit Fernet key if used during encryption")
    passphrase: Optional[str] = Field(None, description="Passphrase if encrypted with passphrase")


class DecryptResponse(SQLModel):
    plaintext: str = Field(..., description="Decrypted original plaintext")
    algorithm: str = Field(default="AES-256 (Fernet)", description="Encryption algorithm")


class AESGCMEncryptRequest(SQLModel):
    text: str = Field(..., description="Plaintext data", examples=["Confidential payload"])
    associated_data: Optional[str] = Field(None, description="Optional associated data for AEAD authenticity", examples=["metadata-header"])


class AESGCMDecryptRequest(SQLModel):
    nonce: str = Field(..., description="Base64 encoded 96-bit nonce")
    ciphertext: str = Field(..., description="Base64 encoded ciphertext")
    associated_data: Optional[str] = Field(None, description="Associated authenticated data if supplied during encryption")


class KeyGenerateResponse(SQLModel):
    key: str = Field(..., description="Cryptographically secure 256-bit base64 key")
    algorithm: str = Field(default="Fernet / AES-256-CBC with HMAC-SHA256")
    instructions: str = Field(default="Store this safely in your .env file as ENCRYPTION_KEY.")


class HashRequest(SQLModel):
    text: str = Field(..., description="Input text to hash", examples=["The quick brown fox"])
    algorithm: str = Field(default="sha256", description="Algorithm: sha256, sha512, or hmac_sha256", examples=["sha256"])
    secret: Optional[str] = Field(None, description="Secret key for HMAC (required if algorithm is hmac_sha256)")


class HashResponse(SQLModel):
    digest: str = Field(..., description="Computed hash hex digest")
    algorithm: str = Field(..., description="Algorithm used")
