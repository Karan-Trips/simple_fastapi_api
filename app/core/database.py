from __future__ import annotations

import logging
from typing import Generator
from sqlalchemy import exc
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

logger = logging.getLogger(__name__)

# Normalize DATABASE_URL for SQLAlchemy compatibility (e.g. Render / Heroku postgres:// fix)
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Configure connect_args based on database dialect
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        db_url,
        echo=False,
        connect_args=connect_args,
        pool_pre_ping=True
    )
except Exception as e:
    logger.warning(
        f"Failed to initialize database with {db_url}. "
        f"Falling back to local SQLite: {e}"
    )
    engine = create_engine(
        "sqlite:///./app.db",
        echo=False,
        connect_args={"check_same_thread": False}
    )


def get_db() -> Generator[Session, None, None]:
    """Dependency yielding a database session and safely closing it after request."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def init_db() -> None:
    """Create all SQLModel tables in database."""
    global engine
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables initialized successfully.")
    except exc.OperationalError as e:
        logger.error(f"Database connection error during table creation: {e}")
        # If external database failed, fallback to sqlite
        if not str(engine.url).startswith("sqlite"):
            logger.warning("Falling back to local SQLite database 'sqlite:///./app.db'")
            engine = create_engine(
                "sqlite:///./app.db",
                echo=False,
                connect_args={"check_same_thread": False}
            )
            SQLModel.metadata.create_all(engine)
