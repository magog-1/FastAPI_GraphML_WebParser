from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Автоматический поиск задач в модуле "app"
celery_app.autodiscover_tasks(["app"])