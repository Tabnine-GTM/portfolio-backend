from datetime import timedelta
from fastapi_login import LoginManager
from passlib.context import CryptContext

from app.config import settings

manager = LoginManager(
    settings.SECRET_KEY, 
    token_url='/auth/login', 
    use_cookie=True, 
    cookie_name= "portfolio_auth",
    default_expiry=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
)
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(plaintext):
    return pwd_context.hash(plaintext)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
