from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext

from db.models.user.user import User
from config.components.logging_config import logger

# Инициализируем контекст для работы с хешами паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля сравнением хешированных паролей.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_username(username: str) -> User:
    """
    Получение пользователя по имени.
    """
    try:
        user = await User.get(username=username)
        return user
    
    except DoesNotExist:
        logger.error(f"Пользователь с именем {username} не найден")
        return None
