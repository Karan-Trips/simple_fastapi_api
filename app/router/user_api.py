from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app import database, schemas
from app.auth_token_genration import (
    create_access_token,
    get_current_user,
    verify_password,
)
from app.response import (
    create_success_response,
    create_not_found_response,
    create_error_response,
)
from app.repositories import user_repo

user_router = APIRouter(tags=["users"])
sch = schemas.BaseResponse


@user_router.get("/fetch", response_model=sch)
async def root_get_users(db: Session = Depends(database.get_db)):
    users = user_repo.get_all_users(db)
    users = sorted(users, key=lambda u: u.id)
    user_list = []
    for u in users:
        user_data = {
            "id": u.id,
            "name": u.name,
            "email": u.email,
        }
        if u.token:
            user_data["token"] = u.token
        if u.todos:
            user_data["todo_list"] = [todo.model_dump() for todo in u.todos]
        user_list.append(user_data)

    return create_success_response("User list fetched", {"users": user_list})


@user_router.post("/register", response_model=sch)
async def register(
    form_data: schemas.UserCreate = Depends(schemas.as_form_user_create),
    db: Session = Depends(database.get_db),
):
    existing = user_repo.get_user_by_name(db, form_data.name)
    if existing:
        return create_error_response("Username already exists")

    user = user_repo.register_user(db, form_data)
    return create_success_response("Registered successfully", {
        "name": user.name,
        "email": user.email
    })


@user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = user_repo.get_user_by_name(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})
    user.token = token
    db.commit()
    db.refresh(user)

    return {"access_token": token, "token_type": "bearer"}


@user_router.post("/userId", response_model=sch)
async def get_user_by_id(
    form_data: schemas.UserIdRequest = Depends(schemas.as_form_user_id),
    db: Session = Depends(database.get_db),
    _: int = Depends(get_current_user)
):
    user = user_repo.get_user_by_id(db, form_data.id)
    if not user:
        return create_not_found_response("User not found")

    return create_success_response("User fetched successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email
    })


@user_router.put("/update/{id}", response_model=sch)
async def update_user(
    id: int,
    form_data: schemas.UserUpdateRequest = Depends(schemas.as_form_user_update),
    db: Session = Depends(database.get_db),
    _: int = Depends(get_current_user)
):
    user = user_repo.update_user(db, id, form_data)
    if not user:
        return create_not_found_response("User not found")

    return create_success_response("User updated successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email
    })


@user_router.post("/deleteById", response_model=sch)
async def delete_user_by_id(
    form_data: schemas.UserIdRequest = Depends(schemas.as_form_user_id),
    db: Session = Depends(database.get_db),
    _: int = Depends(get_current_user)
):
    user = user_repo.get_user_by_id(db, form_data.id)
    if not user:
        return create_not_found_response("User not found")

    deleted_user = user_repo.delete_user(db, form_data.id)

    return create_success_response("User deleted successfully", {
        "name": deleted_user.name,
        "email": deleted_user.email
    })
