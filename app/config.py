from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PRODUCTION: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
