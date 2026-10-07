from __future__ import annotations

# Backward compatibility adapter
from app.admin import UserAdmin, TodoAdmin, setup_admin

__all__ = ["UserAdmin", "TodoAdmin", "setup_admin"]