import os
from environs import Env
from pydantic_settings import BaseSettings

env = Env()
env.read_env()

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "myjwtsecret")
    JWT_ALGORITHM: str = env.str("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")  #время жизни токена в минутах

    SQLALCHEMY_DATABASE_URL: str = env.str("SQLALCHEMY_DATABASE_URL")
    CELERY_BROKER_URL: str = env.str("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = env.str("CELERY_RESULT_BACKEND")

settings = Settings()