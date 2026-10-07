from __future__ import annotations

from typing import List, Optional
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdateRequest
from app.core.security import hash_password


class UserService:
    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        statement = select(User)
        return list(db.exec(statement).all())

    @staticmethod
    def get_user_by_name(db: Session, name: str) -> Optional[User]:
        statement = select(User).where(User.name == name)
        return db.exec(statement).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.get(User, user_id)

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(
        db: Session, user_id: int, data: UserUpdateRequest
    ) -> Optional[User]:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> Optional[User]:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user
