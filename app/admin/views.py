from __future__ import annotations

from sqladmin import Admin, ModelView
from fastapi import FastAPI
from sqlalchemy.engine import Engine
from app.models.user import User
from app.models.todo import Todo


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email, User.is_active, User.created_at]
    column_searchable_list = [User.name, User.email]
    column_sortable_list = [User.id, User.name, User.created_at]
    form_columns = [User.name, User.email, User.is_active]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"


class TodoAdmin(ModelView, model=Todo):
    column_list = [Todo.id, Todo.task, Todo.status, Todo.is_encrypted, Todo.created_at]
    column_searchable_list = [Todo.task]
    column_sortable_list = [Todo.id, Todo.status, Todo.created_at]
    form_columns = [Todo.task, Todo.status, Todo.user_id, Todo.secret_note]
    name = "Todo"
    name_plural = "Todos"
    icon = "fa-solid fa-list-check"


def setup_admin(app: FastAPI, engine: Engine) -> Admin:
    """Configures and mounts SQLAdmin dashboard onto the FastAPI application."""
    admin = Admin(app, engine, title="FastAPI Control Center")
    admin.add_view(UserAdmin)
    admin.add_view(TodoAdmin)
    return admin
