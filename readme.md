### Документация проекта

---

## 1. Технологический стек
**Backend:**
- **Python 3.12** (основной язык)
- **FastAPI** (веб-фреймворк для API)
- **Tortoise ORM** (работа с БД)
- **Redis** (кэширование/сессии)
- **Pydantic** (валидация данных)
- **Poetry** (управление зависимостями)
- **Alembic** (миграции БД)
- **Babel** (интернационализация)
- **Pillow** (обработка изображений)
- **JWT** (аутентификация)
- **Docker** (контейнеризация)

**Frontend:**
- HTML/CSS/JS (базовые шаблоны)
- Webpack (сборка статики, не явно указано, но подразумевается структурой)

**Инфраструктура:**
- Docker Compose (оркестрация)
- Nginx/Uvicorn (развёртывание)
- GitHub Actions/GitLab CI (CI/CD, на основе файлов *.yml)

**Тестирование:**
- pytest (модульные/интеграционные тесты)
- pytest-cov (покрытие кода)

---

## 2. Архитектура проекта
Проект реализован по принципам **Clean Architecture** с разделением на слои:
- **API Layer**: Роутеры и обработчики запросов
- **Domain Layer**: Бизнес-логика (use_case)
- **Infrastructure Layer**: БД, репозитории, внешние сервисы

### Ключевые компоненты:
| Компонент              | Описание                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `app/api/`             | Все эндпоинты API с версионированием (v1)                              |
| `app/db/`              | Модели БД, миграции, репозитории и Pydantic-схемы                     |
| `app/config/`          | Конфигурация приложения (база, Redis, логирование, среды)             |
| `app/server/`          | Middleware и утилиты сервера (аутентификация, обработка ошибок)       |
| `app/use_case/`        | Бизнес-логика, разделённая по доменам (мастера, салоны, услуги и т.д.)|
| `app/static/`          | Статические файлы (CSS, JS, изображения)                              |
| `app/templates/`       | HTML-шаблоны для SSR                                                 |
| `app/locales/`         | Локализация (поддержка EN/RU)                                        |

---

## 3. Основные модули

### 3.1 Аутентификация и авторизация
- **JWT**-токены для защиты API
- Middleware: `auth_middleware.py`
- Роутеры: `user_login_router.py`, `user_register_router.py`
- Хэндлеры: `jwt_handler.py`, `permissions.py`

### 3.2 Профили мастеров
- **CRUD** операции через `masters_router.py`
- Связь с салонами: `salons_masters_relation_router.py`
- Фото профиля: `photo_avatar_model.py` + оптимизация изображений

### 3.3 Управление салонами
- Вакансии: `vacancies_salons_router.py`
- Приглашения мастеров: `salon_master_invitation_router.py`
- Геолокация: интеграция с городами через `city.py`

### 3.4 Система услуг
- Категории услуг: `service_categories_router.py`
- Стандартные/кастомные услуги: `service_standart_router.py`, `service_custom_router.py`
- Атрибуты услуг: `service_attribute_router.py` (размеры, цвета и т.д.)

---

## 4. Запуск проекта
### Требования:
- Docker + Docker Compose
- Python 3.12
- Poetry

### Инструкция:
```bash
# 1. Клонировать репозиторий
git clone https://github.com/your-project/manicure.git

# 2. Собрать образы
docker-compose -f docker-compose.yml build

# 3. Запустить сервисы
docker-compose -f docker-compose.yml up

# 4. Применить миграции
docker-compose exec web alembic upgrade head

# 5. Загрузить тестовые данные (города)
docker-compose exec web python app/scripts/load_cities.py
```

---

## 5. Примеры запросов API
### Регистрация пользователя:
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "user_type": "master"
}
```

### Получение списка мастеров в городе:
```http
GET /api/v1/moscow/masters
Headers:
  Authorization: Bearer {JWT_TOKEN}
```

---

## 6. Логирование и мониторинг
- Логи разделены на `error.log` и `info.log`
- Формат: JSON с детализацией (время, уровень, сообщение)
- Интеграция с Sentry/Prometheus (возможна через конфиг)

---

## 7. Тестирование
Запуск тестов:
```bash
poetry run pytest tests/ --cov=app --cov-report=html
```

**Покрытие:**
- API endpoints (тесты в `test_api/`)
- Бизнес-логика (`test_utils/`)
- Интеграционные тесты (`test_server/`)

---

## 8. Локализация
Поддержка 2 языков (EN/RU):
- Переводы в `app/locales/`
- Команда для обновления:
```bash
pybabel extract -F babel.cfg -o locales/messages.pot .
pybabel update -i locales/messages.pot -d locales -l ru
```

---

## 9. Лицензия
Проект распространяется под лицензией MIT. Полный текст доступен в файле `LICENSE`.