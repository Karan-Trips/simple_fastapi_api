from __future__ import annotations

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Metadata
    PROJECT_NAME: str = "FastAPI Core & Cryptographic Suite"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_DESCRIPTION: str = """
<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; margin-bottom: 20px;">
  <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; font-family: sans-serif;">FastAPI 0.115+</span>
  <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; font-family: sans-serif;">AES-256 GCM AEAD</span>
  <span style="background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; font-family: sans-serif;">PostgreSQL / SQLModel</span>
  <span style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; font-family: sans-serif;">JWT Bearer Auth</span>
  <span style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; font-family: sans-serif;">Real-time WebSockets</span>
</div>

High-performance production API engineered with clean architecture, enterprise cryptographic primitives, and real-time event broadcasting.

---

### 🔑 Quick Authorization Guide
1. **Get Token**: Open the **Authentication & Users** group below and execute `POST /auth/login` (or `/auth/register` first).
2. **Copy Value**: Copy the `access_token` returned in the response.
3. **Authorize**: Click the **Authorize 🔓** button at the top right, enter `Bearer <your_token>`, and click **Authorize**.

---

### 🌐 Quick Resources
* ⚡ **Scalar Interactive Reference**: [`/scalar`](/scalar)
* 📊 **SQLAdmin Dashboard**: [`/admin`](/admin)
* 💬 **WebSocket Test Sender**: [`/static/sender.html`](/static/sender.html)
* 📡 **WebSocket Test Receiver**: [`/static/receiver.html`](/static/receiver.html)
* 💚 **Health Diagnostics**: [`/health`](/health)
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
