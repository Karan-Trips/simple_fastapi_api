from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="Unique username")
    email: str = Field(index=True, unique=True, description="User email address")
    password: str = Field(description="Bcrypt hashed password")
    token: Optional[str] = Field(default=None, description="Active session JWT token")
    is_active: bool = Field(default=True, description="Account active status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Account creation timestamp"
    )

    # Relationship to Todos
    todos: List["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
