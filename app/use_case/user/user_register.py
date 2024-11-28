from tortoise.exceptions import IntegrityError
from pydantic import ValidationError

from db.repositories.user_repositories.user_repositories import UserRepository
from config.components.logging_config import logger


async def register_user(username: str, email: str, password: str, city_id: str, role: str):
    try:
        user = await UserRepository.create_user(username, email, password, city_id, role)
        return user
    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        raise ValidationError("Пользователь с таким именем или email уже существует.")
    except ValidationError as e:
        logger.error(f"Ошибка валидации данных: {e}")
        raise