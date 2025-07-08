# app/routers/todo.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from app import database, schemas
from app.auth_token_genration import get_current_user
from app.response import (
    create_success_response,
    create_not_found_response,
    create_error_response,
)
from app.repositories import todo_repo

todo_router = APIRouter(tags=["Todo"])
sch = schemas.BaseResponse


@todo_router.post("/create")
async def create_todo(
    todo_data: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user),
):
    todo = todo_repo.create_todo(db, user_id, todo_data)
    if not todo:
        return create_error_response("User not found")
    return create_success_response("Todo created successfully", todo.model_dump())


@todo_router.get("/fetch-todo")
async def fetch_todo(
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user)
):
    todos = todo_repo.fetch_todos_by_user(db, user_id)
    if todos is None:
        return create_error_response("User not found")
    return create_success_response("Todo fetched successfully", {
        "todos": [todo.model_dump() for todo in todos]
    })


@todo_router.delete("/delete-todo")
async def delete_todo(
    todo_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user),
):
    todo = todo_repo.delete_todo(db, user_id, todo_id)
    if not todo:
        return create_not_found_response("Todo not found")
    return create_success_response("Todo deleted successfully", todo.model_dump())


@todo_router.put("/update-todo")
async def update_todo(
    todo_id: int,
    todo_data: schemas.TodoUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user),
):
    todo = todo_repo.update_todo(db, user_id, todo_id, todo_data)
    if not todo:
        return create_not_found_response("Todo not found")
    return create_success_response("Todo updated successfully", todo.model_dump())


@todo_router.put("/update-todo-status")
async def update_todo_status(
    todo_id: int,
    todo_data: schemas.TodoUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(get_current_user),
):
    todo = todo_repo.update_todo_status(db, user_id, todo_id, todo_data.status)
    if not todo:
        return create_not_found_response("Todo not found")
    return create_success_response("Todo status updated successfully", todo.model_dump())
