from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from app.schemas.crypto import (
    EncryptRequest, DecryptRequest,
    AESGCMEncryptRequest, AESGCMDecryptRequest,
    HashRequest
)
from app.schemas.common import BaseResponse
from app.services.crypto_service import CryptoService
from app.utils.response import create_success_response

crypto_router = APIRouter(prefix="/crypto", tags=["Cryptography & Security"])


@crypto_router.get(
    "/generate-key",
    response_model=BaseResponse,
    summary="Generate Cryptographic 256-bit Key",
    description="Generates a cryptographically random 256-bit URL-safe base64 key suitable for AES-256 / Fernet encryption."
)
async def generate_key():
    new_key = CryptoService.generate_key()
    return create_success_response(
        "Generated secure 256-bit encryption key",
        {
            "key": new_key,
            "algorithm": "AES-256 (Fernet / CBC + HMAC)",
            "usage": "Use this key in your .env as ENCRYPTION_KEY or provide it in encrypt/decrypt requests."
        }
    )


@crypto_router.post(
    "/encrypt",
    response_model=BaseResponse,
    summary="Encrypt Plaintext",
    description="""
Encrypts sensitive text using **AES-256 / Fernet**.
* **Default**: Uses the secure server encryption key configured in the environment.
* **Custom Key**: Supply a 256-bit Fernet key in the `key` parameter.
* **Passphrase**: Supply a human-readable password in `passphrase` for PBKDF2-HMAC-SHA256 key derivation.
"""
)
async def encrypt_data(payload: EncryptRequest):
    try:
        res = CryptoService.encrypt_data(payload.text, key=payload.key, passphrase=payload.passphrase)
        return create_success_response("Data encrypted successfully", res)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Encryption error: {str(exc)}"
        )


@crypto_router.post(
    "/decrypt",
    response_model=BaseResponse,
    summary="Decrypt Ciphertext",
    description="""
Decrypts ciphertext produced by the encrypt endpoint back to the original plaintext.
Matches the method used during encryption (server key, custom key, or passphrase).
"""
)
async def decrypt_data(payload: DecryptRequest):
    try:
        plaintext = CryptoService.decrypt_data(payload.ciphertext, key=payload.key, passphrase=payload.passphrase)
        return create_success_response(
            "Data decrypted successfully",
            {
                "plaintext": plaintext,
                "algorithm": "AES-256 (Fernet)"
            }
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decryption failed: {str(exc)}"
        )


@crypto_router.post(
    "/aes-gcm/encrypt",
    response_model=BaseResponse,
    summary="AES-256-GCM AEAD Encrypt",
    description="Encrypts plaintext using **AES-256-GCM** (Galois/Counter Mode with Authenticated Data)."
)
async def encrypt_gcm(payload: AESGCMEncryptRequest):
    try:
        result = CryptoService.encrypt_gcm(
            text=payload.text,
            associated_data=payload.associated_data
        )
        return create_success_response("AES-256-GCM encryption successful", result)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@crypto_router.post(
    "/aes-gcm/decrypt",
    response_model=BaseResponse,
    summary="AES-256-GCM AEAD Decrypt",
    description="Decrypts an **AES-256-GCM** ciphertext and verifies authenticity tag."
)
async def decrypt_gcm(payload: AESGCMDecryptRequest):
    try:
        plaintext = CryptoService.decrypt_gcm(
            nonce_b64=payload.nonce,
            ciphertext_b64=payload.ciphertext,
            associated_data=payload.associated_data
        )
        return create_success_response("AES-256-GCM decryption successful", {"plaintext": plaintext})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@crypto_router.post(
    "/hash",
    response_model=BaseResponse,
    summary="Cryptographic Hash & Digest",
    description="Calculates SHA-256, SHA-512, or HMAC-SHA256 digests."
)
async def calculate_hash(payload: HashRequest):
    try:
        digest = CryptoService.compute_hash(payload.text, algorithm=payload.algorithm, secret=payload.secret)
        return create_success_response("Hash computed successfully", {
            "digest": digest,
            "algorithm": payload.algorithm.lower().replace("-", "_")
        })
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
