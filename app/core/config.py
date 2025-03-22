import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "myjwtsecret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # время жизни токена в минутах

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

settings = Settings()