========================================
DJANGO REST FRAMEWORK CHECKLIST
========================================

1. Создание проекта в PyCharm
----------------------------------------
File -> New Project
Custom environment -> Generate new -> Type: Poetry
Base Python: C:\Path\to\python.exe
Poetry: C:\Users\Username\AppData\Roaming\Python\Scripts\poetry.exe
Project location: C:\Projects\ProjectName


2. Активация виртуального окружения
----------------------------------------
Windows: poetry shell
Linux/Mac: source .venv/bin/activate


3. Базовые зависимости
----------------------------------------
poetry add django djangorestframework psycopg[binary] python-dotenv


4. Создание БД PostgreSQL
----------------------------------------
psql -U postgres
CREATE DATABASE dbname;
CREATE USER dbuser WITH PASSWORD 'dbpassword';
ALTER ROLE dbuser SET client_encoding TO 'utf8';
ALTER ROLE dbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dbname TO dbuser;
\q


5. Создание .env в корне проекта
----------------------------------------
DEBUG=True
SECRET_KEY=django-insecure-change-me-123456789
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=dbname
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432


6. Инициализация Django-проекта
----------------------------------------
poetry run django-admin startproject config .


7. Настройка dotenv в manage.py
----------------------------------------
Замените содержимое manage.py на:

#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()


8. Настройка config/settings.py
----------------------------------------
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


9. Настройка wsgi.py
----------------------------------------
import os
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


10. Настройка asgi.py
----------------------------------------
import os
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.core.asgi import get_asgi_application
application = get_asgi_application()


11. Проверка подключения к БД
----------------------------------------
poetry run python manage.py migrate


12. Создание приложения core
----------------------------------------
poetry run python manage.py startapp core


13. Создание структуры для тестов
----------------------------------------
mkdir core/tests
touch core/tests/__init__.py
touch core/tests/test_models.py
touch core/tests/test_views.py


14. Регистрация приложения в settings.py
----------------------------------------
Добавить 'core' в INSTALLED_APPS


15. Создание модели (core/models.py)
----------------------------------------
from django.db import models

class Message(models.Model):
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.email} - {self.created_at}"


16. Создание сериализатора (core/serializers.py)
----------------------------------------
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'email', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


17. Создание ViewSet (core/views.py)
----------------------------------------
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer


18. Настройка маршрутов (core/urls.py)
----------------------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


19. Подключение к проекту (config/urls.py)
----------------------------------------
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
]


20. Миграции
----------------------------------------
poetry run python manage.py makemigrations
poetry run python manage.py migrate


21. Создание суперпользователя
----------------------------------------
poetry run python manage.py createsuperuser


22. Регистрация модели в админке (core/admin.py)
----------------------------------------
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['email', 'text']


23. Установка инструментов разработки
----------------------------------------
poetry add --group lint flake8 mypy black isort
poetry add --group lint django-stubs
poetry add --group dev pytest pytest-cov pytest-django
poetry add --group dev pre-commit


24. Настройка pyproject.toml (добавить в конец)
----------------------------------------
[tool.black]
line-length = 119
target-version = ["py312"]

[tool.isort]
profile = "black"
line_length = 119
multi_line_output = 3
include_trailing_comma = true

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true
disallow_untyped_defs = true
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "config.settings"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
python_files = ["test_*.py", "tests/test_*.py"]
addopts = "--reuse-db --cov=core --cov-report=term-missing"

[tool.coverage.run]
source = ["core"]
omit = ["*/migrations/*", "*/tests/*"]

[tool.coverage.report]
fail_under = 80


25. Настройка .flake8 (создать файл в корне)
----------------------------------------
[flake8]
max-line-length = 119
ignore = E203, E501, W503
exclude = .git, __pycache__, venv, .venv, migrations, node_modules
per-file-ignores =
    */__init__.py:F401


26. Настройка pre-commit (создать .pre-commit-config.yaml)
----------------------------------------
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]

Установка: poetry run pre-commit install


27. Создание .gitignore
----------------------------------------
Взять шаблон: https://github.com/github/gitignore/blob/main/Python.gitignore
Добавить:
.env
*.db
staticfiles/
media/
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/


28. Инициализация Git
----------------------------------------
git init
git branch -M main
git add .
git commit -m "Initial Django REST Framework project"


29. Создание репозитория на GitHub
----------------------------------------
git remote add origin git@github.com:UserName/ProjectName.git
git push -u origin main


30. Создание ветки develop
----------------------------------------
git checkout -b develop
git push -u origin develop


31. Запуск сервера
----------------------------------------
poetry run python manage.py runserver

Проверить:
- API: http://127.0.0.1:8000/api/messages/
- Browsable API: http://127.0.0.1:8000/api/
- Админка: http://127.0.0.1:8000/admin/


32. Написание первого теста (core/tests/test_views.py)
----------------------------------------
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Message

class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_message(self):
        url = '/api/messages/'
        data = {'email': 'test@example.com', 'text': 'Hello World'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)


33. Запуск тестов
----------------------------------------
poetry run pytest -v

```text
========================================
ФИНАЛЬНАЯ СТРУКТУРА ПРОЕКТА
========================================

ProjectName/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
│   ├── migrations/
│   ├── tests/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── static/
├── media/
├── templates/
├── .env
├── .gitignore
├── .flake8
├── .pre-commit-config.yaml
├── pyproject.toml
├── poetry.lock
└── manage.py


========================================
========================================
```