Документация проекта
Введение
Этот проект представляет собой платформу для управления мастерами, салонами и услугами. 
В данной документации описаны основные компоненты системы, используемые технологии и структура проекта.
Структура проекта
Проект организован в виде модульной структуры, что позволяет легко расширять и поддерживать код. 

Основные директории и их назначение:

app: Основной каталог приложения.

api: Содержит API-маршруты и контроллеры.
v1: Версия API.
auth: Маршруты для аутентификации и регистрации пользователей.
cities: Маршруты для работы с городами.
job: Маршруты для работы с вакансиями и заявками.
masters: Маршруты для управления мастерами.
salons: Маршруты для управления салонами.
services: Маршруты для управления услугами.
config: Конфигурационные файлы и настройки.
components: Компоненты конфигурации (база данных, логирование и т.д.).
envs: Конфигурации для различных окружений (разработка, продакшн).
db: Модели базы данных и миграции.
models: Модели данных.
repositories: Репозитории для работы с базой данных.
schemas: Схемы данных.
use_case: Бизнес-логика и сервисы.
base_services: Базовые сервисы.
city_service: Сервисы для работы с городами.
job_service: Сервисы для работы с вакансиями и заявками.
master_service: Сервисы для работы с мастерами.
photo_service: Сервисы для работы с фотографиями.
salon_service: Сервисы для работы с салонами.
service_service: Сервисы для работы с услугами.
user: Сервисы для работы с пользователями.
utils: Утилиты и вспомогательные функции.
babel.cfg: Конфигурация для интернационализации.

data: Папка для хранения данных.

docker: Docker-конфигурации.

locales: Локализации.

main.py: Точка входа в приложение.

Makefile: Файл для автоматизации задач.

media: Медиафайлы.

poetry.lock и pyproject.toml: Файлы конфигурации Poetry для управления зависимостями.

readme.md: Основной файл документации.

server: Конфигурации сервера.

static: Статические файлы (CSS, JS и т.д.).

templates: HTML-шаблоны.

tests: Тесты.

Описание.txt: Описание проекта.




# FastAPI Docker Boilerplate


This project is based on [FastAPI Docker Boilerplate](https://github.com/Afaneor/fastapi-docker-boilerplate).

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Translations](#translations)
- [CI/CD](#cicd)

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
3. Configure the environment variables in the `.env` file

## Running the Application

### Locally

```shell
python3 app/main.py
```

### Using Docker

```shell
docker-compose up -d
```

## Configuration

Project settings are divided into components and environments (development/production). They are located in the `app/config/components/` directory.

The main logic for combining settings is in the `__init__.py` file.

To switch between environments, change the `ENVIRONMENT` variable in the `.env` file.

## Database Migrations

The project uses [Tortoise ORM](https://github.com/tortoise/tortoise-orm) and [Aerich](https://github.com/tortoise/aerich) for managing migrations.

### Initializing Migrations

```shell
aerich init-db
```

This will create a migrations folder in the db module. All models in `__init__.py` (db module) will be reflected in the migration.

### Creating a New Migration

```shell
aerich migrate
```

### Applying Migrations

```shell
aerich upgrade
```

## Translations

The project supports internationalization using FastAPI-Babel and Pybabel. Translation files are managed using Make commands for easy maintenance.

### Translation Management Commands

1. **Extract Translatable Strings**
   ```shell
   make translations-extract
   ```
   This will scan your project and create/update the message template (POT) file.

2. **Initialize a New Language**
   ```shell
   make translations-init LANG=xx
   ```
   Replace `xx` with the language code (e.g., `ru` for Russian, `de` for German).

3. **Compile Translation Messages**
   ```shell
   make translations-compile
   ```
   Compiles the translation files for use in the application.

4. **Update Existing Translations**
   ```shell
   make translations-update
   ```
   Updates existing translation files with new strings found in the code.

5. **Complete Translation Workflow**
   ```shell
   make translations-all LANG=xx
   ```
   Runs the complete workflow for a new language: extract strings, initialize language, and compile messages.

### Translation File Structure
- `/app/locales/`: Directory containing all translation files
- `/app/locales/messages.pot`: Template file containing all translatable strings
- `/app/locales/<lang>/LC_MESSAGES/`: Language-specific translation files

### Using Translations in Code
The project uses FastAPI-Babel for handling translations. You can use the translation system in your code like this:

```python
from fastapi_babel import _
# In your route or model:
message = _("Your message to translate")
```

## CI/CD

The project includes a basic CI/CD configuration using GitLab CI. The `.gitlab-ci.yml` file contains stage for building image of the application.