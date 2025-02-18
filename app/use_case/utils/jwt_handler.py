from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from config.components.logging_config import logger
from config.envs.development import Settings


settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  # Укажите путь для логина

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Создаёт JWT токен.
    :param data: Данные для кодирования в токен.
    :param expires_delta: Время жизни токена.
    :return: Сгенерированный JWT токен.
    """
    logger.info(f"Начало создания JWT токена для данных: {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "city": data.get("city", ""),  # Добавление города
        "role": data.get("role", ""),  # Роль пользователя
        "is_confirmed": data.get("is_confirmed", False),  # флаг подтверждения email
    })

    # Ensure 'sub' is a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    try:
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.info(f"JWT токен успешно создан: {encoded_jwt}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Ошибка при создании JWT токена: {e}")
        raise


def decode_access_token(token: str) -> dict:
    """
    Декодирует JWT токен.
    :param token: JWT токен.
    :return: Раскодированные данные.
    """
    logger.info(f"Начало декодирования JWT токена: {token}")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        logger.info(f"Токен успешно декодирован: {payload}")

        # Принудительно в строку иначе ошибка
        if "sub" in payload:
            payload["sub"] = str(payload["sub"])

        # Проверка на истечение срока действия
        if "exp" in payload and datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            logger.warning("Токен истек.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

        return payload
    except JWTError as e:
        logger.error(f"Ошибка декодирования токена: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    logger.info(f"Получение текущего пользователя из токена.")
    try:
        payload = decode_access_token(token)
        logger.info(f"Декодированный токен: {payload}")
        user_id = payload.get("sub")  # Это теперь user_id, а не login
        if not user_id:
            logger.warning("User ID отсутствует в токене.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not payload.get("is_confirmed", False):  # Проверяем, подтверждён ли email
            logger.warning(f"Пользователь {user_id} не подтвердил email.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email не подтвержден. Пожалуйста, подтвердите свой email.",
            )

        user_data = {
            "username": payload.get("username", "Unknown"),
            "user_id": user_id,
            "role": payload.get("role", ""),
            "city_id": payload.get("city_id"),  # Если есть city_id в токене
            "is_confirmed": payload.get("is_confirmed", False),  # Добавляем в ответ
        }
        logger.info(f"Текущий пользователь: {user_data}")
        return user_data
    except JWTError as e:
        logger.error(f"Ошибка получения текущего пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def create_confirmation_token(user_id: int, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Создаёт JWT токен для подтверждения email.
    :param user_id: ID пользователя.
    :param expires_delta: Время жизни токена.
    :return: Сгенерированный JWT токен.
    """

    # Проверка типа expires_delta, чтобы избежать ошибок при сложении
    if isinstance(expires_delta, str):
        # Преобразуем строку в timedelta (например, из строки "24 hours")
        expires_delta = timedelta(hours=int(expires_delta.split()[0]))  # Примерная логика

    # Если expires_delta всё равно None, устанавливаем значение по умолчанию
    expiration = datetime.utcnow() + (expires_delta or timedelta(hours=24))  # По умолчанию 24 часа

    to_encode = {
        "sub": user_id,
        "exp": expiration,
        "is_confirmed": False,  # Флаг подтверждения email
    }

    try:
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.info(f"Токен для подтверждения email успешно создан для user_id={user_id}.")
        return encoded_jwt

    except Exception as e:
        logger.error(f"Ошибка при создании токена для подтверждения email: {e}")
        raise

def decode_confirmation_token(token: str) -> dict:
    """
    Декодирует JWT токен подтверждения email.
    :param token: JWT токен.
    :return: Раскодированные данные.
    """
    logger.info(f"Начало декодирования JWT токена подтверждения email: {token}")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        logger.info(f"Токен подтверждения email успешно декодирован: {payload}")

        # Проверка на истечение срока действия (оставить как есть)
        if "exp" in payload and datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            logger.warning("Токен истек.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

        return payload
    except JWTError as e:
        logger.error(f"Ошибка декодирования токена подтверждения email: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )