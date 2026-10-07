from __future__ import annotations

# Backward compatibility repository module wrapping TodoService
from app.services.todo_service import TodoService

create_todo = TodoService.create_todo
fetch_todos_by_user = TodoService.fetch_todos_by_user
delete_todo = TodoService.delete_todo
update_todo = TodoService.update_todo
update_todo_status = TodoService.update_todo_status

__all__ = [
    "create_todo",
    "fetch_todos_by_user",
    "delete_todo",
    "update_todo",
    "update_todo_status",
]
