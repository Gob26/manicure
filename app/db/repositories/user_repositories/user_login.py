from fastapi import HTTPException
from passlib.context import CryptContext
from db.models.user.user import User
from config.components.logging_config import logger
from tortoise.exceptions import DoesNotExist


# Инициализируем контекст для работы с хешами паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAuthService:
    """
    Сервис для работы с аутентификацией пользователей.
    """

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверка пароля сравнением хешированных паролей.
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Ошибка при проверке пароля: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при проверке пароля")
