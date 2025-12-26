# Установка и запуск
1. Установка зависимостей
   
   Через uv:
   ```bash
   uv sync
   ```
   Через pip:
   ```bash
   pip install -r requirements.txt
   ```
2. Запуск Redis
   ```bash
   redis-server
   ```
3. Запуск Celery worker
   ```bash
   uv run celery -A project worker -l info
   ```
   Либо же:
   ```bash
   celery -A project worker -l info
   ```
4. Миграции (при первом запуске)
   Через uv:
   ```bash
   uv run manage.py makemigrations && uv run manage.py migrate
   ```
   Через python:
   ```bash
   python manage.py makemigrations && python manage.py migrate
   ```
5. Запуск Django
   
   Через uv:
   ```bash
   uv run manage.py runserver
   ```
   Через python:
   ```bash
   python manage.py runserver
   ```