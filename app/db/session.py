from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # только для SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
