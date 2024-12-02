from passlib.context import CryptContext
from tortoise.exceptions import IntegrityError
from pydantic import ValidationError

from db.repositories.user_repositories.user_repositories import UserRepository
from config.components.logging_config import logger

# Инициализируем контекст для работы с хешами паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def register_user(username: str, email: str, password: str, city_name: str, role: str):
    try:
        logger.info(f"Пользователь {username} пытается зарегистрироваться с городом {city_name}")

        if await UserRepository.get_user_by_username(username):
            logger.warning(f"Пользователь с таким именем уже существует: {username}")
            raise ValidationError("username_exists", "Пользователь с таким именем уже существует")

        if await UserRepository.get_user_by_email(email):
            logger.warning(f"Пользователь с таким email уже существует: {email}")
            raise ValidationError("email_exists", "Пользователь с таким email уже существует")

        city = await UserRepository.get_city_by_name(city_name)
        if not city:
            logger.error(f"Город с названием {city_name} не найден")
            raise ValidationError("city_not_found", f"Город с названием {city_name} не найден")

        logger.info(f"Город {city_name} найден, ID: {city.id}")

        hashed_password = hash_password(password)
        user = await UserRepository.create_user(
            username=username,
            email=email,
            password=hashed_password,
            city_name=city_name,  # передаем название города
            role=role
        )

        logger.info(f"Пользователь {username} успешно зарегистрирован.")
        return user
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя {username}: {str(e)}")
        raise

