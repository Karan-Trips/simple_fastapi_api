from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import Form
from pydantic import EmailStr, Field
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str = Field(..., min_length=2, max_length=50, description="Username", examples=["alice_dev"])
    email: EmailStr = Field(..., description="Unique email address", examples=["alice@example.com"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain text password (will be hashed)", examples=["P@ssw0rd123!"])


def as_form_user_create(
    name: str = Form(..., description="Username"),
    email: EmailStr = Form(..., description="User Email"),
    password: str = Form(..., description="User Password")
) -> UserCreate:
    return UserCreate(name=name, email=email, password=password)


class UserLogin(SQLModel):
    email: EmailStr = Field(..., examples=["alice@example.com"])
    password: str = Field(..., examples=["P@ssw0rd123!"])


def as_form_user_login(
    email: EmailStr = Form(...),
    password: str = Form(...)
) -> UserLogin:
    return UserLogin(email=email, password=password)


class UserIdRequest(SQLModel):
    id: int = Field(..., description="Target User ID", examples=[1])


def as_form_user_id(id: int = Form(...)) -> UserIdRequest:
    return UserIdRequest(id=id)


class UserUpdateRequest(SQLModel):
    name: Optional[str] = Field(None, examples=["alice_updated"])
    email: Optional[EmailStr] = Field(None, examples=["alice_new@example.com"])


def as_form_user_update(
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None)
) -> UserUpdateRequest:
    return UserUpdateRequest(name=name, email=email)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
