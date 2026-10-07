from __future__ import annotations

# Backward compatibility adapter
from app.api.v1.todos import todos_router as todo_router

__all__ = ["todo_router"]
