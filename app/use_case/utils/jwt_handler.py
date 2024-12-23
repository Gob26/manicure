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
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "city": data.get("city", ""),  # Добавление города
        "role": data.get("role", ""),  # Роль пользователя
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt



def decode_access_token(token: str) -> dict:
    """
    Декодирует JWT токен.
    :param token: JWT токен.
    :return: Раскодированные данные.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        # Проверка на истечение срока действия
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_access_token(token)
        logger.info(f"Декодированный токен: {payload}")  # Добавьте логирование для токена
        user_id = payload.get("sub")  # Это теперь user_id, а не login
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "username": payload.get("username", "Unknown"),
            "user_id": user_id,
            "role": payload.get("role", ""),
            "city_id": payload.get("city_id"),  # Если есть city_id в токене
        }
    except JWTError as e:
        logger.error(f"Ошибка декодирования токена: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )