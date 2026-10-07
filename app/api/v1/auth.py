from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, verify_password
from app.schemas.user import UserCreate, as_form_user_create
from app.schemas.common import BaseResponse
from app.services.user_service import UserService
from app.utils.response import create_created_response, create_success_response

auth_router = APIRouter(tags=["Authentication & Users"])


@auth_router.post(
    "/register",
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Registers a new user account with secure password hashing."
)
async def register(
    form_data: UserCreate = Depends(as_form_user_create),
    db: Session = Depends(get_db),
):
    if UserService.get_user_by_name(db, form_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken."
        )

    if UserService.get_user_by_email(db, form_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already registered."
        )

    user = UserService.register_user(db, form_data)
    return create_created_response(
        "User registered successfully",
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
    )


@auth_router.post(
    "/login",
    summary="OAuth2 / JWT User Login",
    description="Authenticates credentials and issues a signed JWT access token. Integrates with Swagger UI Authorize button."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_name(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": str(user.id), "username": user.name})
    user.token = token
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.name
    }


@auth_router.post(
    "/logout",
    response_model=BaseResponse,
    summary="User Logout",
    description="Invalidates current user session by clearing active token."
)
async def logout(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.token = None
    db.add(user)
    db.commit()
    db.refresh(user)

    return create_success_response("Logged out successfully", {
        "id": user.id,
        "name": user.name,
        "email": user.email
    })
