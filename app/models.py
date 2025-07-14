from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    token: Optional[str] = None
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str
    status: bool = False
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="todos")

