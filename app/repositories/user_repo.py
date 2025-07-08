from sqlalchemy.orm import Session
from app import models, schemas
from app.auth_token_genration import hash_password

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def register_user(db: Session, user_data: schemas.UserCreate):
    new_user = models.User(
        name=user_data.name,
        password=hash_password(user_data.password),
        email=user_data.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, data: schemas.UserUpdateRequest):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
