from __future__ import annotations

import logging
from typing import List, Optional
from sqlmodel import Session, select
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate
from app.core import crypto

logger = logging.getLogger(__name__)


class TodoService:
    @staticmethod
    def create_todo(db: Session, user_id: int, todo_data: TodoCreate) -> Optional[Todo]:
        user = db.get(User, user_id)
        if not user:
            return None

        secret_note_val = todo_data.secret_note
        is_encrypted = False

        if secret_note_val and todo_data.encrypt_note:
            try:
                secret_note_val = crypto.encrypt_text(secret_note_val)
                is_encrypted = True
            except Exception as e:
                logger.error(f"Error encrypting secret note: {e}")

        todo = Todo(
            task=todo_data.task,
            status=todo_data.status,
            secret_note=secret_note_val,
            is_encrypted=is_encrypted,
            user_id=user_id,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def fetch_todos_by_user(db: Session, user_id: int, decrypt_notes: bool = True) -> Optional[List[dict]]:
        user = db.get(User, user_id)
        if not user:
            return None

        statement = select(Todo).where(Todo.user_id == user_id)
        todos = list(db.exec(statement).all())

        results = []
        for t in todos:
            item = t.model_dump()
            if decrypt_notes and t.is_encrypted and t.secret_note:
                try:
                    item["secret_note_decrypted"] = crypto.decrypt_text(t.secret_note)
                except Exception:
                    item["secret_note_decrypted"] = "[Decryption Error]"
            results.append(item)

        return results

    @staticmethod
    def delete_todo(db: Session, user_id: int, todo_id: int) -> Optional[Todo]:
        todo = db.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return None
        db.delete(todo)
        db.commit()
        return todo

    @staticmethod
    def update_todo(
        db: Session, user_id: int, todo_id: int, todo_data: TodoUpdate
    ) -> Optional[Todo]:
        todo = db.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return None

        if todo_data.task is not None:
            todo.task = todo_data.task
        if todo_data.status is not None:
            todo.status = todo_data.status
        if todo_data.secret_note is not None:
            if todo_data.encrypt_note:
                todo.secret_note = crypto.encrypt_text(todo_data.secret_note)
                todo.is_encrypted = True
            else:
                todo.secret_note = todo_data.secret_note
                todo.is_encrypted = False

        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def update_todo_status(
        db: Session, user_id: int, todo_id: int, status: bool
    ) -> Optional[Todo]:
        todo = db.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return None
        todo.status = status
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
