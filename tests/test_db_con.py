import asyncio
import asyncpg
from config import DatabaseConfig

async def test_postgres_connection():
    db_config = DatabaseConfig()
    connection_string = db_config.postgres_connection_string

    try:
        # Подключаемся к базе данных PostgreSQL
        conn = await asyncpg.connect(dsn=connection_string)
        print("Успешное подключение к базе данных!")
        await conn.close()
    except Exception as e:
        print(f"Ошибка при подключении: {e}")

# Запускаем тестовое подключение
asyncio.run(test_postgres_connection())
