from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.todo import TodoCreate, TodoUpdate
from app.schemas.common import BaseResponse
from app.services.todo_service import TodoService
from app.utils.response import create_created_response, create_success_response

todos_router = APIRouter(tags=["Todo & Task Management"])


@todos_router.post(
    "/create",
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Todo (Legacy Endpoint)",
    description="Creates a task with optional AES-256 encrypted note."
)
@todos_router.post(
    "/todos",
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Todo (RESTful Endpoint)"
)
async def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    todo = TodoService.create_todo(db, user_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="User account not found.")

    return create_created_response("Todo created successfully", todo.model_dump())


@todos_router.get(
    "/fetch-todo",
    response_model=BaseResponse,
    summary="Fetch User Todos (Legacy Endpoint)"
)
@todos_router.get(
    "/todos",
    response_model=BaseResponse,
    summary="Fetch User Todos (RESTful Endpoint)",
    description="Fetches tasks for authenticated user with automated AES-256 note decryption."
)
async def fetch_todos(
    decrypt_notes: bool = Query(default=True, description="Whether to decrypt confidential notes in response"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    todos = TodoService.fetch_todos_by_user(db, user_id, decrypt_notes=decrypt_notes)
    if todos is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return create_success_response("Todos fetched successfully", {"todos": todos})


@todos_router.delete(
    "/delete-todo",
    response_model=BaseResponse,
    summary="Delete Todo (Legacy Query Param Endpoint)"
)
async def delete_todo_legacy(
    todo_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    todo = TodoService.delete_todo(db, user_id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized.")

    return create_success_response("Todo deleted successfully", todo.model_dump())


@todos_router.delete(
    "/todos/{todo_id}",
    response_model=BaseResponse,
    summary="Delete Todo (RESTful Endpoint)"
)
async def delete_todo_rest(
    todo_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    todo = TodoService.delete_todo(db, user_id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized.")

    return create_success_response("Todo deleted successfully", todo.model_dump())


@todos_router.put(
    "/update-todo",
    response_model=BaseResponse,
    summary="Update Todo (Legacy Query Param Endpoint)"
)
async def update_todo_legacy(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    todo = TodoService.update_todo(db, user_id, todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized.")

    return create_success_response("Todo updated successfully", todo.model_dump())


@todos_router.put(
    "/todos/{todo_id}",
    response_model=BaseResponse,
    summary="Update Todo (RESTful Endpoint)"
)
async def update_todo_rest(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    todo = TodoService.update_todo(db, user_id, todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized.")

    return create_success_response("Todo updated successfully", todo.model_dump())


@todos_router.put(
    "/update-todo-status",
    response_model=BaseResponse,
    summary="Update Todo Status (Legacy Endpoint)"
)
async def update_todo_status(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    status_val = todo_data.status if todo_data.status is not None else False
    todo = TodoService.update_todo_status(db, user_id, todo_id, status_val)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized.")

    return create_success_response("Todo status updated successfully", todo.model_dump())
