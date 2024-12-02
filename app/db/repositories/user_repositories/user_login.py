from fastapi import HTTPException
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
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Ошибка при проверке пароля: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при проверке пароля")


async def get_user_by_username(username: str) -> User:
    """
    Получение пользователя по имени.
    """
    try:
        # Предположим, что у вас есть модель User с полем username
        user = await User.get(username=username)
        return user
    except DoesNotExist:
        logger.error(f"Пользователь с именем {username} не найден в базе данных")
        return None  # Возвращаем None, если пользователь не найден
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя {username}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")
