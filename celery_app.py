from celery import Celery
from app.core.config import settings
from app.services.parse import *

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

@celery_app.task(name="app.services.parse.parse_website_task")
def parse_website_task(url: str, max_depth: int, format: str = "graphml"):
    graph = crawl_website(url, max_depth)
    result = '-'
    if format.lower() == "graphml":
        result = graph_to_graphml(graph)
    # Для добавления других форматов
    return result

# # Автоматический поиск задач в модуле "app"
# celery_app.autodiscover_tasks(["app.services.parse.parse_website_task"])