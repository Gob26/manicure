from core.redis import get_redis_client

def test_redis_connection():
    try:
        redis_client = get_redis_client()
        # Попробуем выполнить команду PING
        response = redis_client.ping()
        print(f"Redis соединение успешно: {response}")
        return True
    except Exception as e:
        print(f"Ошибка соединения с Redis: {e}")
        return False

# Запустите функцию для проверки
test_redis_connection()