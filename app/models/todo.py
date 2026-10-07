from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    task: str = Field(description="Task description")
    status: bool = Field(default=False, description="Completion status (true if done)")
    
    # Encrypted fields support
    is_encrypted: bool = Field(default=False, description="True if task or secret_note is encrypted at rest")
    secret_note: Optional[str] = Field(default=None, description="Confidential AES-256 encrypted note")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Task creation timestamp")
    user_id: int = Field(foreign_key="users.id", description="Owner user ID")

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="todos")
