from config.components.base import BaseConfig
from config.components.db import DatabaseConfig
from config.components.redis import RedisConfig


class ComponentsConfig(BaseConfig, DatabaseConfig, RedisConfig):
    env: str = "development"  # значение по умолчанию

    # Добавляем новые поля со значениями по умолчанию
    jwt_secret_key: str = "super_secure_key_123"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30  # изменил на int, так как это число

    class Config:
        env_file = ".env"

__all__ = ["ComponentsConfig"]