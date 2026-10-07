from __future__ import annotations

from pydantic import Field
from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str = Field(..., description="JWT Bearer token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in_minutes: int = Field(default=60, description="Token duration in minutes")


class TokenData(SQLModel):
    user_id: int
    username: str
