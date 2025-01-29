from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session
from typing import Dict

from app.crud.user import get_user_by_username, create_user
from app.database import get_db
from app.schemas.user import UserCreate, User
from app.schemas.auth import LoginPayload
from app.security import (
    verify_password,
    manager,
    create_tokens,
    set_tokens_cookies,
    clear_tokens_cookies,
    verify_refresh_token,
)


router = APIRouter(prefix="/auth")


@router.post("/login")
def login(
    response: Response,
    payload: LoginPayload,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    user = get_user_by_username(payload.username, db)

    if user is None or not verify_password(payload.password, user.hashed_password):
        raise InvalidCredentialsException

    access_token, refresh_token = create_tokens(user.username)
    set_tokens_cookies(response, access_token, refresh_token)

    return {"message": "Logged in successfully"}


@router.post("/logout")
def logout(response: Response) -> Dict[str, str]:
    clear_tokens_cookies(response)
    return {"message": "Logged out successfully"}


@router.post("/register")
def register(
    response: Response, user: UserCreate, db: Session = Depends(get_db)
) -> Dict[str, str | User]:
    db_user = get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = create_user(db, user)

    access_token, refresh_token = create_tokens(db_user.username)
    set_tokens_cookies(response, access_token, refresh_token)

    return {"message": "User registered and logged in successfully", "user": db_user}


@router.get("/user", response_model=User)
def get_current_user(user: User = Depends(manager)) -> User:
    return user


@router.post("/refresh")
def refresh_token(
    response: Response, refresh_token: str = Cookie(None, alias="refresh_token")
) -> Dict[str, str]:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    username = verify_refresh_token(refresh_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token, new_refresh_token = create_tokens(username)
    set_tokens_cookies(response, new_access_token, new_refresh_token)

    return {"message": "Token refreshed successfully"}
