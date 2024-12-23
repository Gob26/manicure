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
    })
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
        # Проверка на истечение срока действия
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
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
        user_data = {
            "username": payload.get("username", "Unknown"),
            "user_id": user_id,
            "role": payload.get("role", ""),
            "city_id": payload.get("city_id"),  # Если есть city_id в токене
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
