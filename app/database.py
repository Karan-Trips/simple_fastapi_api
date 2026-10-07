from __future__ import annotations

# Backward compatibility re-export from app.core.database
from app.core.database import engine, get_db, init_db

__all__ = ["engine", "get_db", "init_db"]