from fastapi import HTTPException
from db.repositories.user_repositories.user_login import verify_password, get_user_by_username
from config.components.logging_config import logger

# Функция для входа пользователя
async def login(username: str, password: str):
    logger.info(f"Попытка логина для пользователя {username}")

    user = await get_user_by_username(username)
    if not user:
        logger.error(f"Пользователь с именем {username} не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    logger.info(f"Пользователь {username} найден, проверка пароля.")

    if not verify_password(password, user.password):
        logger.error(f"Неверный пароль для пользователя {username}")
        raise HTTPException(status_code=401, detail="Неверный пароль")

    logger.info(f"Пользователь {username} успешно авторизован")
    return user



