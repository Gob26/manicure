from tortoise.exceptions import IntegrityError
from pydantic import ValidationError

from db.repositories.user_repositories.user_repositories import UserRepository
from config.components.logging_config import logger


async def register_user(username: str, email: str, password: str, city_id: str, role: str):
    try:
        # Проверяем уникальность username
        if await UserRepository.get_user_by_username(username):
            logger.error(f"Пользователь с именем {username} уже существует")
            raise ValidationError(f"Пользователь с именем {username} уже существует")
        # Проверяем уникальность email
        if await UserRepository.get_user_by_email(email):
            logger.error(f"Пользователь с email {email} уже существует")
            raise ValidationError(f"Пользователь с email {email} уже существует")
        # Создаем пользователя
        user = await UserRepository.create_user(username, email, password, city_id, role)
        return user
    # Обрабатываем ошибки при создании пользователя
    except IntegrityError as e:
        logger.error(f"Ошибка создания пользователя: {e}")
        raise ValidationError(f"Ошибка создания пользователя: {e}")
    # Обрабатываем ошибки валидации данных
    except ValidationError as e:
        logger.error(f"Ошибка валидации данных: {e}")
        raise