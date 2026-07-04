# DyplomProject - Таблица в формате SPA

## Описание проекта

Tаблицa в формате Single Page Application (SPA), которая отображает данные из базы данных
и обеспечивает пользователю функциональность для сортировки, фильтрации и пагинации данных.

## Технологии

- **Backend:** Django 6.0, Django REST Framework
- **Frontend:** Vue.js, Axios, Bootstrap
- **База данных:** PostgreSQL
- **Документация:** Swagger, Readok

## Установка и запуск

### Требования

- Python 3.11+
- PostgreSQL
- Poetry

## 1. Клонирование репозитория

```bash
git clone https://github.com/botnbot/diplom.git
cd diplom
```
## 2. Установка зависимостей
``` bash
poetry install
```
## 3. Настройка базы данных
Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE skorodb;
CREATE USER skoro WITH PASSWORD 'skoropassword';
ALTER ROLE skoro SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE skorodb TO skoro;
```
## 4. Настройка переменных окружения
Создайте файл .env в корне проекта:

env
```python
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
POSTGRES_DB=skorodb
POSTGRES_USER=skoro
POSTGRES_PASSWORD=skoropassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
## 5. Выполнение миграций
```bash
poetry run python manage.py migrate
```
## 6. Генерация тестовых данных
```bash
poetry run python manage.py generate_data
```
## 7. Создание суперпользователя
```bash
poetry run python manage.py createsuperuser
```
## 8. Запуск сервера
```bash
poetry run python manage.py runserver
```
## 9. Доступ к приложению
Таблица: http://127.0.0.1:8001/

API: http://127.0.0.1:8001/api/items/

Админка: http://127.0.0.1:8001/admin/

Swagger: http://127.0.0.1:8001/swagger/

## 10.Функциональность
Таблица с 4 колонками: Дата, Название, Количество, Расстояние

Сортировка по всем полям (кроме даты)

Фильтрация по названию и количеству

Пагинация (серверная)

## 11.Запуск тестов
```bash
poetry run python manage.py test
```
## Структура проекта
```text
DyplomProject/
├── config/              # Полная структура настроек Django
├── core/                # Основное приложение
│   ├── migrations/      # Миграции БД
│   ├── tests/           # Тесты
│   ├── models.py        # Модели данных
│   ├── views.py         # API views
│   ├── serializers.py   # DRF сериализаторы
│   ├── urls.py          # Маршруты
│   ├── views_.py        # бэкенд API
│   └ views_frontend.py  # фронтенд SPA
├── templates/
│           └─index.html # Главная страница с Vue.js
├──.env                  # Переменные окружения
├── env.example          # Шаблон переменных окружения
├──.gitignore            # Содержит список файлов и папок, которые не должны попадать в репозиторий
├── docker-compose.yml   # Docker Compose конфигурация
├── Dockerfile.simple    # Dockerfile для сборки
├── manage.py            # Управление проектом
├── nginx.conf           # Конфигурация Nginx         
├── poetry.lock          # Фиксация зависимостей Poetry        
├── pyproject.toml       # Зависимости из Poetry
├── README.md            # Описание и инструкции
└── requirements.txt     # Файл с зависимостями


```
Автор
[skoro@smn35.com]