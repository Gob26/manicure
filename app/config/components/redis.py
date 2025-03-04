from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from pathlib import Path

# Определяем путь к .env файлу непосредственно здесь
ENV_FILE_PATH = Path(__file__).parents[3].joinpath('.env')

class RedisConfig(BaseSettings):
    redis_host: str = Field(default='localhost')
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_url: str = Field(default='')

    model_config = {
        'env_file': ENV_FILE_PATH,
        'env_file_encoding': 'utf-8',
        'extra': 'ignore',  # Игнорировать лишние переменные
    }

    @computed_field(return_type=str)
    def redis_connection_string(self):
        return self.redis_url or f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}'

# Создаем экземпляр конфигурации Redis
redis_config = RedisConfig()