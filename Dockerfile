FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей без создания виртуального окружения
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копирование всего проекта
COPY . .

# Создание директории для статики
RUN mkdir -p /app/staticfiles

# Сбор статики
RUN poetry run python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запуск приложения с Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
