# Изолированный conftest.py для автоматического создания тестовой БД в памяти и отката изменений
import pytest
from tortoise.contrib.test import initializer # Импортируем только initializer
from tortoise import Tortoise  # Импортируем Tortoise
from tortoise.transactions import in_transaction
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from typing import Dict, List, Any  # Импортируем типы


# Определяем DatabaseConfig прямо здесь, чтобы изолировать его от внешних настроек
class DatabaseConfig(BaseSettings):
    test_db_url: str = Field(default='sqlite://:memory:')  # Используем SQLite в памяти

    model_config = {
        'env_file': None,  # Отключаем загрузку из .env файла
        'env_file_encoding': 'utf-8',
        'extra': 'ignore', # Игнорируем любые лишние переменные, если вдруг попадут
    }

    @computed_field(return_type=Dict[str, List[str]]) # Явно указываем тип возвращаемого значения
    def apps_for_tests(self) -> Dict[str, List[str]]: # Явно указываем тип возвращаемого значения и добавляем -> Dict[str, List[str]]
        return {
            'server': [
                'db.models', # Укажите путь к вашим моделям
            ],
        }

    @computed_field(return_type=Dict) # <---- Добавляем tortoise_config в DatabaseConfig
    def tortoise_config(self) -> Dict: # <---- Добавляем tortoise_config в DatabaseConfig
        return {
            'connections': {
                'default': self.postgres_connection_string # <----  Хотя postgres_connection_string не используется, tortoise_config нужен
            },
            'apps': self.apps_for_tests(),
        }


db_config = DatabaseConfig() # Создаем экземпляр ИЗОЛИРОВАННОГО DatabaseConfig


async def generate_test_schemas(): # Функция генерации схем (теперь вне initializer)
    await Tortoise.init(db_url=db_config.test_db_url, modules=db_config.apps_for_tests(), config=db_config.tortoise_config) # <---- Передаем config=db_config.tortoise_config
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    """
    Автоматически создает тестовую базу данных (SQLite в памяти) и откатывает изменения после тестов.
    Полностью изолирован от внешних конфигураций.
    """
    test_db_url = db_config.test_db_url # Теперь всегда будет sqlite://:memory:

    # Генерируем схемы ПЕРЕД initializer -  теперь вызываем напрямую, без run_async
    await generate_test_schemas() # <-----  Вызываем асинхронную функцию напрямую

    # Инициализация тестовой базы (теперь без generate_schemas)
    initializer(db_config.apps_for_tests(), db_url=test_db_url) # Вызываем функцию, чтобы получить словарь

    async with in_transaction() as connection:
        yield  # Запускаем тесты

        # Откатываем транзакцию после теста
        await connection.rollback()

    # Завершаем соединение с базой -  используем Tortoise.close_connections() вместо finalizer()
    await Tortoise.close_connections() # <---- Заменяем finalizer() на Tortoise.close_connections()
    # await finalizer() # <---- УДАЛЯЕМ finalizer()