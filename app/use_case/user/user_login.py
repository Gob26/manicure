from fastapi import HTTPException
from db.repositories.user_repositories.user_login import verify_password, get_user_by_username
from config.components.logging_config import logger
from jose import jwt
from datetime import datetime, timedelta
from config.envs.development import Settings
from use_case.utils.jwt_handler import create_access_token

# Загружаем настройки из Settings
settings = Settings()

# Функция для входа пользователя
async def login(username: str, password: str):
    logger.info(f"Попытка логина для пользователя {username}")

    # Получаем пользователя по имени
    user = await get_user_by_username(username)
    if not user:
        logger.error(f"Пользователь с именем {username} не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    logger.info(f"Пользователь {username} найден, проверка пароля.")

    # Проверяем пароль
    if not verify_password(password, user.password):
        logger.error(f"Неверный пароль для пользователя {username}")
        raise HTTPException(status_code=401, detail="Неверный пароль")

    logger.info(f"Пользователь {username} успешно авторизован")

    # Сначала получаем город и city_id
    city_name = None
    city_id = None
    if user.city:
        try:
            city = await user.city  # Получаем город пользователя (предполагаем, что это отношение)
            city_name = city.name if city else None
            city_id = city.id if city else None  # Извлекаем city_id
        except Exception as e:
            logger.error(f"Ошибка при получении города пользователя: {e}")
            city_name = None
            city_id = None

    # Генерация токена с дополнительными данными
    access_token = create_access_token(data={
        "sub": user.id,
        "username": user.username,
        "role": user.role,
        "city_id": city_id
    })
    # Возвращаем данные о токене и пользователе
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "city": city_name,
        "city_id": city_id
    }