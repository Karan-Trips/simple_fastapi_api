from __future__ import annotations

from typing import Dict, Optional
from app.core import crypto


class CryptoService:
    @staticmethod
    def generate_key() -> str:
        return crypto.generate_encryption_key()

    @staticmethod
    def encrypt_data(text: str, key: Optional[str] = None, passphrase: Optional[str] = None) -> Dict[str, str]:
        if passphrase:
            ciphertext = crypto.encrypt_with_passphrase(text, passphrase)
            method = "pbkdf2_passphrase"
        elif key:
            ciphertext = crypto.encrypt_text(text, custom_key=key)
            method = "custom_fernet_key"
        else:
            ciphertext = crypto.encrypt_text(text)
            method = "server_master_key"

        return {
            "ciphertext": ciphertext,
            "algorithm": "AES-256 (Fernet)",
            "method": method
        }

    @staticmethod
    def decrypt_data(ciphertext: str, key: Optional[str] = None, passphrase: Optional[str] = None) -> str:
        if passphrase:
            return crypto.decrypt_with_passphrase(ciphertext, passphrase)
        elif key:
            return crypto.decrypt_text(ciphertext, custom_key=key)
        else:
            return crypto.decrypt_text(ciphertext)

    @staticmethod
    def encrypt_gcm(text: str, key_b64: Optional[str] = None, associated_data: Optional[str] = None) -> Dict[str, str]:
        return crypto.encrypt_aes_gcm(plaintext=text, key_b64=key_b64, associated_data=associated_data)

    @staticmethod
    def decrypt_gcm(nonce_b64: str, ciphertext_b64: str, key_b64: Optional[str] = None, associated_data: Optional[str] = None) -> str:
        return crypto.decrypt_aes_gcm(nonce_b64=nonce_b64, ciphertext_b64=ciphertext_b64, key_b64=key_b64, associated_data=associated_data)

    @staticmethod
    def compute_hash(text: str, algorithm: str = "sha256", secret: Optional[str] = None) -> str:
        algo = algorithm.lower().replace("-", "_")
        if algo == "sha256":
            return crypto.hash_sha256(text)
        elif algo == "sha512":
            return crypto.hash_sha512(text)
        elif algo == "hmac_sha256":
            if not secret:
                raise ValueError("Secret key is required for HMAC calculation.")
            return crypto.hmac_sha256(text, secret=secret)
        else:
            raise ValueError(f"Unsupported algorithm '{algorithm}'")
