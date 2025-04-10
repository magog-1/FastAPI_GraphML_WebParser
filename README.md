# Парсинг сайта и построение графа

## Описание функциональности:

1. Парсинг начинается с указанного URL и рекурсивно обходит все внутренние ссылки до заданной глубины.
2. Каждая уникальная страница становится узлом в графе, а ссылки между страницами - рёбрами.
3. Результирующий граф сохраняется в выбранном формате (например, GraphML).

## Начало работы

    • Для миграций базы данных с помощью Alembic настройте файл alembic.ini и env.py, указывая путь к models через app/db/base.py.  
    • Запуск приложения: uvicorn main:app  
    • Запуск воркера Celery: celery -A celery_app.celery_app worker --loglevel=info  (celery -A celery_app.celery_app worker --pool=solo --loglevel=info)
    • Не забудьте установить и запустить Redis для работы Celery.
    • Документация доступна http://localhost:8000/docs
    • Примеры запросов находятся в requests.txt