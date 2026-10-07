from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class TodoCreate(SQLModel):
    task: str = Field(..., min_length=1, max_length=255, description="Task title or description", examples=["Complete cryptographic audit"])
    status: bool = Field(default=False, description="Completion status", examples=[False])
    secret_note: Optional[str] = Field(default=None, description="Optional sensitive note to be encrypted", examples=["Top secret task info"])
    encrypt_note: bool = Field(default=True, description="Whether to encrypt secret_note using AES-256 at rest", examples=[True])


class TodoUpdate(SQLModel):
    task: Optional[str] = Field(None, description="Updated task title", examples=["Updated task description"])
    status: Optional[bool] = Field(None, description="Updated completion status", examples=[True])
    secret_note: Optional[str] = Field(None, description="Updated secret note", examples=["Updated secret info"])
    encrypt_note: bool = Field(default=True, description="Whether to encrypt secret_note at rest")


class TodoRead(SQLModel):
    id: int
    task: str
    status: bool
    is_encrypted: bool
    secret_note: Optional[str] = None
    created_at: datetime
    user_id: int


class TodoId(SQLModel):
    id: int = Field(..., examples=[1])
