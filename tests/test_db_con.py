import asyncio
from tortoise import Tortoise
from config.components.db import DatabaseConfig
from config.components.logging_config import logger

async def test_postgres_connection():
    """
    Тестирование подключения к базе данных PostgreSQL с использованием Tortoise.
    """
    db_config = DatabaseConfig()

    logger.debug(f"Проверка строки подключения: {db_config.postgres_connection_string.replace('postgres://', 'postgres://***:***@')}")

    # Конфигурация Tortoise для тестирования подключения
    config = {
        'connections': {
            'default': db_config.postgres_connection_string
        },
        'apps': {
            'models': {
                'models': [],  # Убираем модели, чтобы просто протестировать соединение
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': 'UTC'
    }

    try:
        # Инициализация подключения к базе данных
        await Tortoise.init(config=config)
        logger.info("Успешное подключение к базе данных!")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {str(e)}")
    finally:
        # Закрытие всех соединений после проверки
        await Tortoise.close_connections()
        logger.info("Соединение закрыто.")

if __name__ == "__main__":
    asyncio.run(test_postgres_connection())
