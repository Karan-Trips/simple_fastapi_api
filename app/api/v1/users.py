from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import (
    UserIdRequest, UserUpdateRequest,
    as_form_user_id, as_form_user_update
)
from app.schemas.common import BaseResponse
from app.services.user_service import UserService
from app.utils.response import create_success_response

users_router = APIRouter(tags=["Authentication & Users"])


@users_router.get(
    "/fetch",
    response_model=BaseResponse,
    summary="Fetch All Users (Legacy Endpoint)",
    description="Returns list of all registered users with their todos."
)
@users_router.get(
    "/users",
    response_model=BaseResponse,
    summary="List All Users (RESTful Endpoint)"
)
async def get_all_users(db: Session = Depends(get_db)):
    users = UserService.get_all_users(db)
    users = sorted(users, key=lambda u: (u.id if u.id is not None else float('inf')))
    user_list = []
    for u in users:
        user_data = {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_active": u.is_active,
            "created_at": str(u.created_at) if u.created_at else None,
        }
        if u.token:
            user_data["token"] = u.token
        if u.todos:
            user_data["todo_list"] = [todo.model_dump() for todo in u.todos]
        user_list.append(user_data)

    return create_success_response("User list fetched successfully", {"users": user_list})


@users_router.post(
    "/userId",
    response_model=BaseResponse,
    summary="Fetch User By ID (Legacy Form Endpoint)"
)
async def get_user_by_id_legacy(
    form_data: UserIdRequest = Depends(as_form_user_id),
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user)
):
    user = UserService.get_user_by_id(db, form_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("User fetched successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email
    })


@users_router.get(
    "/users/{id}",
    response_model=BaseResponse,
    summary="Fetch User By ID (RESTful Endpoint)"
)
async def get_user_by_id_rest(
    id: int,
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user)
):
    user = UserService.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("User fetched successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": str(user.created_at) if user.created_at else None,
    })


@users_router.put(
    "/update/{id}",
    response_model=BaseResponse,
    summary="Update User Profile (Legacy & REST Path)"
)
async def update_user(
    id: int,
    form_data: UserUpdateRequest = Depends(as_form_user_update),
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user)
):
    user = UserService.update_user(db, id, form_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("User updated successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email
    })


@users_router.post(
    "/deleteById",
    response_model=BaseResponse,
    summary="Delete User (Legacy Form Endpoint)"
)
async def delete_user_by_id_legacy(
    form_data: UserIdRequest = Depends(as_form_user_id),
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user)
):
    deleted_user = UserService.delete_user(db, form_data.id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("User deleted successfully", {
        "name": deleted_user.name,
        "email": deleted_user.email
    })


@users_router.delete(
    "/users/{id}",
    response_model=BaseResponse,
    summary="Delete User (RESTful Endpoint)"
)
async def delete_user_by_id_rest(
    id: int,
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user)
):
    deleted_user = UserService.delete_user(db, id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("User deleted successfully", {
        "id": deleted_user.id,
        "name": deleted_user.name,
        "email": deleted_user.email
    })
