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
        if await UserRepository.get_user_by_username(username):
            raise ValidationError("username_exists", "Пользователь с таким именем уже существует")
        
        if await UserRepository.get_user_by_email(email):
            raise ValidationError("email_exists", "Пользователь с таким email уже существует")
        
        city = await UserRepository.get_city_by_name(city_name)
        if not city:
            raise ValidationError("city_not_found", f"Город {city_name} не найден")
        
        hashed_password = hash_password(password)
        return await UserRepository.create_user(
            username, 
            email, 
            hashed_password, 
            city.id,  # Используем city.id вместо city_id
            role
        )
    except IntegrityError as e:
        logger.error(f"Database integrity error: {str(e)}")
        raise ValidationError("database_error", "Ошибка при создании пользователя")
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise