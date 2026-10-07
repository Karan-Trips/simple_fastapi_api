from __future__ import annotations

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Metadata
    PROJECT_NAME: str = "Simple FastAPI Core & Cryptographic API"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_DESCRIPTION: str = """
# 🚀 Simple FastAPI Core & Cryptographic Suite

Welcome to the upgraded **FastAPI API** with enterprise-grade security, AES-256 encryption & decryption, JWT authentication, and interactive API documentation.

### ✨ Key Features
* 🔐 **JWT Authentication & RBAC**: Bearer tokens with configurable expiration and bcrypt password hashing.
* 🛡️ **Military-Grade Encryption**: AES-256 / Fernet symmetric encryption, AES-GCM AEAD, and PBKDF2 key derivation.
* 📝 **Todo & Task Management**: Full CRUD with encrypted secret notes.
* ⚡ **Real-time WebSockets**: Multi-client chat and notification broadcasting at `/ws`.
* 📊 **Admin Dashboard**: Interactive SQLAdmin database interface at `/admin`.
* 📖 **Dual Interactive Documentation**:
  * **Custom Swagger UI**: [`/docs`](/docs)
  * **Scalar Modern API Reference**: [`/scalar`](/scalar)
  * **ReDoc Documentation**: [`/redoc`](/redoc)

---
### 🔑 How to Authenticate in Swagger UI
1. Go to the **Authentication** section below and execute `POST /login` with your credentials (or `POST /register` first).
2. Copy the returned `access_token`.
3. Click the **Authorize 🔓** button at the top right of this page.
4. Enter `Bearer <your_token>` (or just paste the token in OAuth2) and click **Authorize**.
"""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database: defaults to SQLite for zero-setup execution, configurable via .env for PostgreSQL / MySQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Security & JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "7e9f78792102ff35b0243c694c5602807618e85c96e8e8c37c2e0940aa3700c4"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Cryptography (256-bit AES / Fernet key)
    ENCRYPTION_KEY: str = os.getenv(
        "ENCRYPTION_KEY", 
        "Jr364QnDUZYS3xYw4sjVGB_J0a0xHXCx8F6f99R-5UU="
    )

    # CORS Configuration (for live frontend / API access)
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS or self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
