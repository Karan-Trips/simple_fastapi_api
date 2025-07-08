from fastapi import Form
from pydantic import EmailStr
from sqlmodel import SQLModel, Field 
from typing import Optional, Dict

class BaseResponse(SQLModel):
    code: int
    message: str
    data: Optional[Dict] = None

class TodoCreate(SQLModel):
    task: str
    status: bool


class TodoUpdate(SQLModel):
    task: str
    status: bool


class TodoId(SQLModel):
    id: int


# ////////////////////////////////////_____________USER_________///////////////////////////////////

class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str

def as_form_user_create(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
) -> UserCreate:
    return UserCreate(name=name, email=email, password=password)

class UserLogin(SQLModel):
    email: EmailStr
    password: str

def as_form_user_login(
    email: EmailStr = Form(...),
    password: str = Form(...)
) -> UserLogin:
    return UserLogin(email=email, password=password)

class UserIdRequest(SQLModel):
    id: int

def as_form_user_id(id: int = Form(...)) -> UserIdRequest:
    return UserIdRequest(id=id)

class UserUpdateRequest(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

def as_form_user_update(
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None)
) -> UserUpdateRequest:
    return UserUpdateRequest(name=name, email=email)
