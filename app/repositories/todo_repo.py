

from sqlalchemy.orm import Session
from app import models, schemas

def create_todo(db: Session, user_id: int, todo_data: schemas.TodoCreate):
    user = db.get(models.User, user_id)
    if not user:
        return None

    todo = models.Todo(**todo_data.model_dump())
    user.todos.append(todo)
    db.add(user)
    db.commit()
    db.refresh(todo)
    return todo

def fetch_todos_by_user(db: Session, user_id: int):
    user = db.get(models.User, user_id)
    if not user:
        return None
    return user.todos

def delete_todo(db: Session, user_id: int, todo_id: int):
    todo = db.get(models.Todo, todo_id)
    if not todo or todo.user_id != user_id:
        return None
    db.delete(todo)
    db.commit()
    return todo

def update_todo(db: Session, user_id: int, todo_id: int, todo_data: schemas.TodoUpdate):
    todo = db.get(models.Todo, todo_id)
    if not todo or todo.user_id != user_id:
        return None
    todo.task = todo_data.task
    todo.status = todo_data.status
    db.commit()
    db.refresh(todo)
    return todo

def update_todo_status(db: Session, user_id: int, todo_id: int, status: bool):
    todo = db.get(models.Todo, todo_id)
    if not todo or todo.user_id != user_id:
        return None
    todo.status = status
    db.commit()
    db.refresh(todo)
    return todo
