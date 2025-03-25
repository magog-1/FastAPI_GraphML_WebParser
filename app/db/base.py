from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Импорт моделей для регистрации (для alembic)
from app.models import user