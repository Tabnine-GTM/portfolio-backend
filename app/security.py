from datetime import timedelta
from typing import Tuple
from fastapi import Response
from fastapi_login import LoginManager
from passlib.context import CryptContext
import jwt

from app.config import settings

manager = LoginManager(
    settings.SECRET_KEY,
    token_url="/auth/login",
    use_cookie=True,
    cookie_name="portfolio_auth",
    default_expiry=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
)
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(plaintext: str) -> str:
    return pwd_context.hash(plaintext)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_tokens(username: str) -> Tuple[str, str]:
    access_token = manager.create_access_token(
        data={"sub": username},
        expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = manager.create_access_token(
        data={"sub": username},
        expires=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return access_token, refresh_token


def set_tokens_cookies(
    response: Response, access_token: str, refresh_token: str
) -> None:
    manager.set_cookie(response, access_token)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.PRODUCTION,  # Only set secure=True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


def clear_tokens_cookies(response: Response) -> None:
    response.delete_cookie(
        key=manager.cookie_name,
        httponly=True,
        secure=settings.PRODUCTION,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token", httponly=True, secure=settings.PRODUCTION, samesite="lax"
    )


def verify_refresh_token(refresh_token: str) -> str | None:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str | None = payload.get("sub")
        return username if username else None
    except jwt.PyJWTError:
        return None
