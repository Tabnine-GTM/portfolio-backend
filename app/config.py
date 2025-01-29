from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PRODUCTION: bool = False
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5173",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
