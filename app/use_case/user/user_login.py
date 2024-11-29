from fastapi import HTTPException
from db.repositories.user_repositories.user_login import verify_password, get_user_by_username
from config.components.logging_config import logger

# Функция для входа пользователя
async def login(username: str, password: str):
    user = await get_user_by_username(username)
    # Проверяем, что пользователь существует
    if not user:
        logger.error(f"Пользователь с именем {username} не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Сравниваем введённый пароль с хешированным паролем из базы данных
    if not verify_password(password, user.password):
        logger.error(f"Неверный пароль для пользователя {username}")
        raise HTTPException(status_code=401, detail="Неверный пароль")
    
    return user


