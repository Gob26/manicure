import pytest
from app.core.redis import get_redis_client

@pytest.mark.asyncio
async def test_redis_connection():
    """Проверяем подключение к Redis"""
    try:
        redis_client = get_redis_client()

        # Проверка ping
        response = await redis_client.ping()
        assert response is True, "Redis ping failed"

        # Проверка записи и чтения
        test_value = "test_value"
        await redis_client.set("test_key", test_value)
        result = await redis_client.get("test_key")

        # Убираем .decode(), так как данные уже являются строками
        decoded_result = result if result else None
        assert decoded_result == test_value, f"Expected {test_value}, got {decoded_result}"

        print("✅ Соединение с Redis работает корректно!")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        pytest.fail(f"Не удалось подключиться к Redis: {e}")
    finally:
        # Очистка тестовых данных
        await redis_client.delete("test_key")