from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
