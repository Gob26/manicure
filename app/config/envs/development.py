# config/envs/development.py
from pydantic_settings import BaseSettings
from config.constants import ENV_FILE_PATH


class DevelopmentConfig(BaseSettings):
    env: str = 'development'
    reload: bool = True
    workers: int = 2

    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # CORS settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    use_sentry: bool = False

    sender_email: str
    sender_password: str
    base_url: str = "http://localhost:8000"  # Добавляем базовый URL

    model_config = {
        'env_file': ENV_FILE_PATH,
        'env_file_encoding': 'utf-8',
    }


class Settings(BaseSettings):
    # Основные настройки приложения
    app_name: str = "Manicure Catalog"
    debug: bool = True
    version: str = "1.0.0"

    # JWT настройки
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # PostgreSQL настройки
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_port: str = "5433"
    postgres_db: str = "manicure_db"

    # Redis
    redis_host: str = "localhost"
    redis_port: str = "6379"
    redis_db: str = "0"

    # Environment
    env: str = "development"

    # Настройки для отправки email
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    BASE_URL: str = "http://localhost:8000"  # Добавляем базовый URL

    model_config = {
        'env_file': ENV_FILE_PATH,
        'env_file_encoding': 'utf-8'
    }